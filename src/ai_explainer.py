def explain_failure(analysis):
    """Prepare a structured explanation from rule-based analysis."""

    return {
        "failure_type": analysis["failure_type"],
        "severity": analysis["severity"],
        "summary": analysis["message"],
        "evidence": analysis["evidence"],
        "suggestion": analysis["suggestion"],
        "ai_generated": False,
    }
