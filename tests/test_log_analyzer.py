import unittest

from src.log_analyzer import analyze_log


class TestLogAnalyzer(unittest.TestCase):

    def test_detects_test_failure(self):
        result = analyze_log("AssertionError: Expected 100, received 120.")

        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["failure_type"], "Test Failure")

    def test_detects_dependency_failure(self):
        result = analyze_log("ModuleNotFoundError: No module named 'requests'")

        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["failure_type"], "Dependency Failure")

    def test_detects_timeout(self):
        result = analyze_log("TimeoutError: Operation timed out")

        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["failure_type"], "Timeout")

    def test_unknown_failure(self):
        result = analyze_log("Pipeline completed with no recognized errors.")

        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["failure_type"], "Unclassified")

    def test_empty_log(self):
        result = analyze_log("")

        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["failure_type"], "Unclassified")


if __name__ == "__main__":
    unittest.main()
