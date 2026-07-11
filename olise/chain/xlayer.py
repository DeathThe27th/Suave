"""X Layer testnet commitment layer.

Compiles + deploys OliseCommit once (address persisted in .olise_chain.json),
then commits report hashes before kickoff and settles them after full time.
If contract deployment fails 3 times, falls back to embedding hashes in
self-transaction calldata (documented in DECISIONS.md).
"""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

from eth_utils import keccak
from web3 import Web3

from olise import config

log = logging.getLogger("olise.chain")

SOL_PATH = Path(__file__).resolve().parent / "OliseCommit.sol"
SOLC_VERSION = "0.8.24"


def commitment_hash(pdf_bytes: bytes, canonical_forecasts_json: str) -> str:
    return "0x" + keccak(pdf_bytes + canonical_forecasts_json.encode()).hex()


class ChainClient:
    def __init__(self):
        self.w3 = None
        self.account = None
        self.contract = None
        self.mode = "disabled"        # contract | calldata | disabled
        self.address = None
        self.chain_id = None
        self._lock = asyncio.Lock()

    # ------------------------------------------------------------------
    def _connect(self):
        for rpc in config.XLAYER_RPCS:
            try:
                w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 20}))
                cid = w3.eth.chain_id
                self.w3, self.chain_id = w3, cid
                log.info("chain: connected to %s (chain id %s)", rpc, cid)
                return
            except Exception as e:
                log.warning("chain: RPC %s unreachable: %s", rpc, str(e)[:120])
        raise RuntimeError("no X Layer testnet RPC reachable")

    def _compile(self) -> dict:
        import solcx
        if SOLC_VERSION not in [str(v) for v in solcx.get_installed_solc_versions()]:
            solcx.install_solc(SOLC_VERSION)
        out = solcx.compile_source(
            SOL_PATH.read_text(),
            output_values=["abi", "bin"],
            solc_version=SOLC_VERSION,
        )
        return next(v for k, v in out.items() if k.endswith(":OliseCommit"))

    def _send(self, tx: dict) -> str:
        tx.setdefault("from", self.account.address)
        tx.setdefault("nonce", self.w3.eth.get_transaction_count(self.account.address))
        tx.setdefault("chainId", self.chain_id)
        if "maxFeePerGas" not in tx and "maxPriorityFeePerGas" not in tx:
            tx.setdefault("gasPrice", self.w3.eth.gas_price)
        if "gas" not in tx:
            tx["gas"] = int(self.w3.eth.estimate_gas(tx) * 1.3)
        signed = self.account.sign_transaction(tx)
        h = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(h, timeout=120)
        if receipt.status != 1:
            raise RuntimeError(f"tx reverted: {h.hex()}")
        return "0x" + h.hex().removeprefix("0x")

    # ------------------------------------------------------------------
    def _setup_sync(self):
        self._connect()
        self.account = self.w3.eth.account.from_key(config.XLAYER_PRIVATE_KEY)
        bal = self.w3.eth.get_balance(self.account.address)
        log.info("chain: operator %s balance %s OKB",
                 self.account.address, self.w3.from_wei(bal, "ether"))

        compiled = self._compile()
        abi = compiled["abi"]

        state = {}
        if config.CHAIN_STATE_FILE.exists():
            state = json.loads(config.CHAIN_STATE_FILE.read_text())
        addr = config.OLISE_CONTRACT_ADDRESS or state.get("contract_address")
        if addr and self.w3.eth.get_code(addr):
            self.contract = self.w3.eth.contract(address=addr, abi=abi)
            self.address, self.mode = addr, "contract"
            log.info("chain: using existing OliseCommit at %s", addr)
            return

        for attempt in range(1, 4):
            try:
                factory = self.w3.eth.contract(abi=abi, bytecode=compiled["bin"])
                tx = factory.constructor().build_transaction({
                    "from": self.account.address,
                    "nonce": self.w3.eth.get_transaction_count(self.account.address),
                    "chainId": self.chain_id,
                    "gasPrice": self.w3.eth.gas_price,
                })
                signed = self.account.sign_transaction(tx)
                h = self.w3.eth.send_raw_transaction(signed.raw_transaction)
                receipt = self.w3.eth.wait_for_transaction_receipt(h, timeout=180)
                if receipt.status != 1:
                    raise RuntimeError("deploy tx reverted")
                self.address = receipt.contractAddress
                self.contract = self.w3.eth.contract(address=self.address, abi=abi)
                self.mode = "contract"
                config.CHAIN_STATE_FILE.write_text(json.dumps({
                    "contract_address": self.address,
                    "deploy_tx": "0x" + h.hex().removeprefix("0x"),
                    "chain_id": self.chain_id,
                }, indent=2))
                log.info("chain: deployed OliseCommit at %s", self.address)
                return
            except Exception as e:
                log.warning("chain: deploy attempt %d failed: %s", attempt, str(e)[:200])
        self.mode = "calldata"
        log.warning("chain: falling back to calldata commitments")

    async def setup(self):
        try:
            await asyncio.to_thread(self._setup_sync)
        except Exception as e:
            self.mode = "disabled"
            log.error("chain: setup failed, commitments disabled: %s", str(e)[:200])

    # ------------------------------------------------------------------
    async def commit(self, report_hash: str, report_id: str) -> dict:
        async with self._lock:
            return await asyncio.to_thread(self._commit_sync, report_hash, report_id)

    def _commit_sync(self, report_hash: str, report_id: str) -> dict:
        if self.mode == "contract":
            tx = self.contract.functions.commit(
                Web3.to_bytes(hexstr=report_hash), report_id
            ).build_transaction({"from": self.account.address})
            txh = self._send(tx)
        elif self.mode == "calldata":
            payload = json.dumps({"olise_commit": report_hash, "report_id": report_id})
            txh = self._send({
                "to": self.account.address, "value": 0,
                "data": "0x" + payload.encode().hex(),
            })
        else:
            raise RuntimeError("chain commitments unavailable")
        return {
            "hash": report_hash,
            "tx_hash": txh,
            "explorer_url": config.EXPLORER_TX.format(tx=txh),
            "mode": self.mode,
            "contract_address": self.address,
        }

    async def settle(self, report_hash: str, results_uri: str,
                     correct: int, total: int) -> dict:
        async with self._lock:
            return await asyncio.to_thread(
                self._settle_sync, report_hash, results_uri, correct, total)

    def _settle_sync(self, report_hash, results_uri, correct, total) -> dict:
        if self.mode == "contract":
            tx = self.contract.functions.settle(
                Web3.to_bytes(hexstr=report_hash), results_uri, correct, total
            ).build_transaction({"from": self.account.address})
            txh = self._send(tx)
        elif self.mode == "calldata":
            payload = json.dumps({"olise_settle": report_hash,
                                  "results_uri": results_uri,
                                  "correct": correct, "total": total})
            txh = self._send({
                "to": self.account.address, "value": 0,
                "data": "0x" + payload.encode().hex(),
            })
        else:
            raise RuntimeError("chain settlements unavailable")
        return {"tx_hash": txh, "explorer_url": config.EXPLORER_TX.format(tx=txh)}

    # ------------------------------------------------------------------
    def health(self) -> dict:
        out = {"mode": self.mode, "chain_id": self.chain_id,
               "contract_address": self.address}
        try:
            if self.w3 and self.account:
                bal = self.w3.eth.get_balance(self.account.address)
                out["operator"] = self.account.address
                out["balance_okb"] = str(self.w3.from_wei(bal, "ether"))
                out["ok"] = True
            else:
                out["ok"] = False
        except Exception as e:
            out["ok"] = False
            out["error"] = str(e)[:120]
        return out
