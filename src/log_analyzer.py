import json
import sys
from pathlib import Path


def analyze_log(log_text):
    """Identify common CI/CD pipeline failures."""

    if "AssertionError" in log_text or "FAILED" in log_text:
        return {
            "status": "FAILED",
            "failure_type": "Test Failure",
            "message": "A test failed. Check the assertion and expected values."
        }

    elif "ModuleNotFoundError" in log_text or "ImportError" in log_text:
        return {
            "status": "FAILED",
            "failure_type": "Dependency Failure",
            "message": "A Python module could not be imported. Check dependencies."
        }

    elif "TimeoutError" in log_text or "timed out" in log_text.lower():
        return {
            "status": "FAILED",
            "failure_type": "Timeout",
            "message": "An operation exceeded its time limit. Investigate execution time."
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
