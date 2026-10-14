import unittest

from src.ai_explainer import explain_failure
from src.log_analyzer import analyze_log


class TestAIExplainer(unittest.TestCase):
    def test_explanation_uses_analysis_results(self):
        analysis = analyze_log(
            "ModuleNotFoundError: No module named 'requests'"
        )

        result = explain_failure(analysis)

        self.assertEqual(result["failure_type"], "Dependency Failure")
        self.assertEqual(result["severity"], "high")
        self.assertIn("requirements.txt", result["suggestion"])
        self.assertFalse(result["ai_generated"])


if __name__ == "__main__":
    unittest.main()
