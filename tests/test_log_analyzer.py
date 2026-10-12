import unittest

from src.log_analyzer import analyze_log


class TestLogAnalyzer(unittest.TestCase):

    def test_detects_test_failure(self):
        log_text = """
        Running automated tests...
        FAILED test_payment.py::test_payment_total
        AssertionError: Expected 100, received 120.
        """

        result = analyze_log(log_text)

        self.assertEqual(result["status"], "FAILED")
        self.assertEqual(result["failure_type"], "Test Failure")

    def test_unknown_failure(self):
        log_text = "Pipeline completed with no recognized errors."

        result = analyze_log(log_text)

        self.assertEqual(result["status"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
