from pathlib import Path
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

    def test_sample_test_failure_log(self):
        log_path = Path("sample_logs/test_failure.log")
        result = analyze_log(log_path.read_text(encoding="utf-8"))

        self.assertEqual(result["failure_type"], "Test Failure")

    def test_sample_dependency_failure_log(self):
        log_path = Path("sample_logs/dependency_failure.log")
        result = analyze_log(log_path.read_text(encoding="utf-8"))

        self.assertEqual(result["failure_type"], "Dependency Failure")

    def test_sample_timeout_failure_log(self):
        log_path = Path("sample_logs/timeout_failure.log")
        result = analyze_log(log_path.read_text(encoding="utf-8"))

        self.assertEqual(result["failure_type"], "Timeout")

    def test_detects_lowercase_test_failure(self):
        log_text = "failed test_payment.py"

        result = analyze_log(log_text)

        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["failure_type"], "Test Failure")

    def test_detects_lowercase_timeout(self):
        log_text = "the operation timed out"

        result = analyze_log(log_text)

        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["failure_type"], "Timeout")

    def test_detects_lowercase_dependency_failure(self):
        log_text = "modulenotfounderror: no module named 'requests'"

        result = analyze_log(log_text)

        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["failure_type"], "Dependency Failure")

    def test_returns_evidence_for_dependency_failure(self):
        log_text = (
            "Installing dependencies...\n"
            "ModuleNotFoundError: No module named 'requests'\n"
            "Pipeline failed."
        )

        result = analyze_log(log_text)

        self.assertEqual(result["failure_type"], "Dependency Failure")
        self.assertEqual(
            result["evidence"],
            "ModuleNotFoundError: No module named 'requests'"
        )
    def test_returns_evidence_for_test_failure(self):
        log_text = (
            "Running tests...\n"
            "AssertionError: Expected 100, received 120.\n"
            "Pipeline failed."
        )
    
        result = analyze_log(log_text)
    
        self.assertEqual(result["failure_type"], "Test Failure")
        self.assertEqual(
            result["evidence"],
            "AssertionError: Expected 100, received 120."
        )

if __name__ == "__main__":
    unittest.main()
