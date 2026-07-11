# Deploying Olise AI on a Windows VPS (native, no Docker)

Target: an always-on 8 GB Windows VPS. Total time ≈ 20 minutes.

## 1. Install Python 3.11+

Download the latest Python 3.11/3.12 installer from https://www.python.org/downloads/windows/
and run it. **Tick "Add python.exe to PATH"** on the first screen. Verify in PowerShell:

```powershell
python --version
```

## 2. Install the GTK3 runtime (required by WeasyPrint)

WeasyPrint needs Pango/Cairo, provided on Windows by the standard GTK3 runtime installer:

- Download: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
  (grab the latest `gtk3-runtime-x.x.x-x-x-x-ts-win64.exe`)
- Run the installer and **tick "Set up PATH environment variable"**.
- Open a **new** PowerShell window afterwards so the PATH change is picked up.

## 3. Get the code and install dependencies

```powershell
cd C:\
git clone <your-repo-url> olise
cd C:\olise
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 4. Create `.env`

Create `C:\olise\.env` (Notepad is fine) with:

```
API_FOOTBALL_KEY=...
GEMINI_API_KEY=...
SUPABASE_URL=https://<ref>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=...
XLAYER_PRIVATE_KEY=0x...        # fresh burner wallet, testnet OKB only
SUPABASE_BUCKET=olise-reports
ADMIN_TOKEN=<pick-a-long-random-string>
HOST=0.0.0.0
PORT=8000
```

Optional: run `schema.sql` once in the Supabase SQL editor to use Supabase
Postgres for persistence; otherwise the service uses a local SQLite file
(`olise_local.db`) automatically.

## 5. First run (foreground)

```powershell
cd C:\olise
.\.venv\Scripts\Activate.ps1
python -m olise.main
```

On first start the service compiles and deploys the `OliseCommit` contract to
X Layer testnet and persists its address in `.olise_chain.json` — keep that file.

### Smoke test

In a second PowerShell window:

```powershell
curl.exe http://127.0.0.1:8000/health
curl.exe -X POST http://127.0.0.1:8000/analyze -H "Content-Type: application/json" -d "{\"home\":\"Spain\",\"away\":\"Belgium\"}"
```

`/health` should report `"status": "ok"` with all checks green.

## 6. Register as an auto-restarting Windows service (NSSM — preferred)

1. Download NSSM from https://nssm.cc/download, unzip, and put `nssm.exe`
   (from the `win64` folder) in `C:\olise\`.
2. In an **elevated** PowerShell:

```powershell
cd C:\olise
.\nssm.exe install OliseAI "C:\olise\.venv\Scripts\python.exe" "-m olise.main"
.\nssm.exe set OliseAI AppDirectory C:\olise
.\nssm.exe set OliseAI AppStdout C:\olise\logs\olise.log
.\nssm.exe set OliseAI AppStderr C:\olise\logs\olise.err.log
.\nssm.exe set OliseAI AppRotateFiles 1
.\nssm.exe set OliseAI Start SERVICE_AUTO_START
.\nssm.exe set OliseAI AppExit Default Restart
mkdir C:\olise\logs -ErrorAction SilentlyContinue
.\nssm.exe start OliseAI
```

The service now starts on boot and restarts automatically if the process dies.
Manage it with `nssm start|stop|restart OliseAI` or `services.msc`.

### Alternative: Task Scheduler

If you can't use NSSM:

```powershell
schtasks /Create /TN "OliseAI" /SC ONSTART /RU SYSTEM /TR "C:\olise\.venv\Scripts\python.exe -m olise.main" /F
schtasks /Run /TN "OliseAI"
```

(Task Scheduler does not restart a crashed process by itself; the built-in
self-ping keeps the service warm but NSSM is the more robust option.)

## 7. Open the firewall port (if serving externally)

```powershell
New-NetFirewallRule -DisplayName "Olise AI" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

## Notes

- The app binds `HOST`/`PORT` from `.env` and uses `pathlib` throughout — the
  same code runs identically on Windows and Linux.
- Back up `.olise_chain.json` (deployed contract address) and, if using the
  SQLite fallback, `olise_local.db`.
- Linux/Render alternatives: `Dockerfile` + `docker-compose.yml`
  (`docker compose up -d`) or `render.yaml`.
