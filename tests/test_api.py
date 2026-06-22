import unittest

try:
    from fastapi.testclient import TestClient
    from backend.tactifit.api import app
except ModuleNotFoundError:  # pragma: no cover - depends on optional local install
    TestClient = None
    app = None


@unittest.skipIf(TestClient is None, "FastAPI is not installed")
class ApiTest(unittest.TestCase):
    def test_root_lists_available_routes(self):
        client = TestClient(app)

        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["docs"], "/docs")

    def test_health(self):
        client = TestClient(app)

        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")


if __name__ == "__main__":
    unittest.main()
