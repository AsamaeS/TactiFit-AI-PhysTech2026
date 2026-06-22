import unittest

try:
    from backend.tactifit import api
except ModuleNotFoundError:  # pragma: no cover - depends on optional local install
    api = None


@unittest.skipIf(api is None, "FastAPI is not installed")
class ApiTest(unittest.TestCase):
    def test_root_lists_available_routes(self):
        response = api.root()

        self.assertEqual(response["app"], "/app")
        self.assertEqual(response["docs"], "/docs")

    def test_health(self):
        response = api.health()

        self.assertEqual(response["status"], "ok")

    def test_coach_app_points_to_frontend_file(self):
        response = api.coach_app()

        self.assertTrue(str(response.path).endswith("frontend\\index.html") or str(response.path).endswith("frontend/index.html"))


if __name__ == "__main__":
    unittest.main()
