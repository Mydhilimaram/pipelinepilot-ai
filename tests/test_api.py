import unittest

from fastapi.testclient import TestClient

from src.api import app


class TestPipelinePilotAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "running")

    def test_analyze_test_failure(self):
        response = self.client.post(
            "/analyze",
            json={
                "log_text": (
                    "FAILED test_payment.py::test_payment_total\n"
                    "AssertionError: Expected total was 100, but received 120."
                )
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "FAILED")
        self.assertEqual(response.json()["failure_type"], "Test Failure")

    def test_analyze_dependency_failure(self):
        response = self.client.post(
            "/analyze",
            json={
                "log_text": (
                    "ModuleNotFoundError: No module named 'requests'"
                )
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["failure_type"], "Dependency Failure")


if __name__ == "__main__":
    unittest.main()
