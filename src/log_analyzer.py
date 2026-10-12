

def analyze_log(log_text):
    """Identify a common CI/CD pipeline failure."""
    if "FAILED" in log_text or "AssertionError" in log_text:
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
