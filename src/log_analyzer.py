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
