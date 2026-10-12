import json
import sys
from pathlib import Path
def analyze_log(log_text):
    """Identify common CI/CD pipeline failures."""

    normalized_log = log_text.lower()

    if (
        "modulenotfounderror" in normalized_log
        or "importerror" in normalized_log
    ):
        return {
            "status": "FAILED",
            "failure_type": "Dependency Failure",
            "message": "A Python module could not be imported. Check dependencies."
        }

    elif (
        "timeouterror" in normalized_log
        or "timed out" in normalized_log
    ):
        return {
            "status": "FAILED",
            "failure_type": "Timeout",
            "message": "An operation exceeded its time limit. Investigate execution time."
        }

    elif (
        "assertionerror" in normalized_log
        or "failed test" in normalized_log
        or "failed test_" in normalized_log
    ):
        return {
            "status": "FAILED",
            "failure_type": "Test Failure",
            "message": "A test failed. Check the assertion and expected values."
        }

    return {
        "status": "UNKNOWN",
        "failure_type": "Unclassified",
        "message": "No recognized failure pattern was found."
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
