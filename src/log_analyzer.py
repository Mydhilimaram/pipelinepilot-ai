import json
import sys
from pathlib import Path


def analyze_log(log_text):
    """Identify common CI/CD failures and provide supporting evidence."""

    normalized_log = log_text.lower()

    if (
        "modulenotfounderror" in normalized_log
        or "importerror" in normalized_log
    ):
        failure_type = "Dependency Failure"
        severity = "high"
        message = (
            "A Python module could not be imported. "
            "Check dependencies."
        )
        patterns = ("modulenotfounderror", "importerror")

    elif (
        "timeouterror" in normalized_log
        or "timed out" in normalized_log
    ):
        failure_type = "Timeout"
        severity = "medium"
        message = (
            "An operation exceeded its time limit. "
            "Investigate execution time."
        )
        patterns = ("timeouterror", "timed out")

    elif (
        "assertionerror" in normalized_log
        or "failed test" in normalized_log
        or "failed test_" in normalized_log
    ):
        failure_type = "Test Failure"
        severity = "medium"
        message = (
            "A test failed. Check the assertion "
            "and expected values."
        )
        patterns = ("assertionerror", "failed test")

    else:
        return {
            "status": "UNKNOWN",
            "failure_type": "Unclassified",
            "severity": "unknown",
            "message": "No recognized failure pattern was found.",
            "evidence": None,
        }

    evidence = next(
        (
            line.strip()
            for line in log_text.splitlines()
            if any(pattern in line.lower() for pattern in patterns)
        ),
        None,
    )
    return {
        "status": "FAILED",
        "failure_type": failure_type,
        "severity": severity,
        "message": message,
        "evidence": evidence,
        "suggestion": (
            "Check requirements.txt and install the missing package."
            if failure_type == "Dependency Failure"
            else "Inspect slow operations, network calls, and timeout settings."
            if failure_type == "Timeout"
            else "Compare expected and actual values and inspect the failing test."
        ),
    }


def main():
    """Read a log file and print its analysis."""

    if len(sys.argv) != 2:
        print("Usage: python -m src.log_analyzer <log_file>")
        sys.exit(1)

    log_path = Path(sys.argv[1])

    try:
        log_text = log_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Error reading log file: {error}", file=sys.stderr)
        sys.exit(1)

    result = analyze_log(log_text)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
