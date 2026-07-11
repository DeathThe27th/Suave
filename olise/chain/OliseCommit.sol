// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title OliseCommit — tamper-proof match research commitments
/// @notice Records the keccak-256 hash of each Olise AI research report
///         (PDF bytes + canonical forecasts JSON) before kickoff, and the
///         graded outcome after full time, building a publicly auditable
///         accuracy record.
contract OliseCommit {
    event ReportCommitted(bytes32 indexed reportHash, string reportId, uint256 timestamp);
    event ReportSettled(bytes32 indexed reportHash, string resultsUri, uint256 correct, uint256 total);

    struct Commitment {
        uint256 committedAt;
        string reportId;
        bool settled;
        uint256 correct;
        uint256 total;
        string resultsUri;
    }

    address public immutable operator;
    mapping(bytes32 => Commitment) public commitments;

    constructor() {
        operator = msg.sender;
    }

    modifier onlyOperator() {
        require(msg.sender == operator, "not operator");
        _;
    }

    function commit(bytes32 reportHash, string calldata reportId) external onlyOperator {
        require(commitments[reportHash].committedAt == 0, "already committed");
        commitments[reportHash] = Commitment(block.timestamp, reportId, false, 0, 0, "");
        emit ReportCommitted(reportHash, reportId, block.timestamp);
    }

    function settle(bytes32 reportHash, string calldata resultsUri, uint256 correct, uint256 total)
        external
        onlyOperator
    {
        Commitment storage c = commitments[reportHash];
        require(c.committedAt != 0, "unknown report");
        require(!c.settled, "already settled");
        c.settled = true;
        c.correct = correct;
        c.total = total;
        c.resultsUri = resultsUri;
        emit ReportSettled(reportHash, resultsUri, correct, total);
    }
}
