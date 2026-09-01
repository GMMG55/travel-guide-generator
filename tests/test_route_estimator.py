import unittest

from scripts.route_estimator import estimate_route, haversine_km


class RouteEstimatorTests(unittest.TestCase):
    def test_haversine_returns_zero_for_same_point(self):
        self.assertEqual(haversine_km([117.1, 36.2], [117.1, 36.2]), 0)

    def test_estimate_route_marks_result_as_estimated(self):
        route = estimate_route([117.1298, 36.2001], [117.1015, 36.2353], "walk")

        self.assertGreater(route["distance_km"], 0)
        self.assertGreater(route["duration_min"], 0)
        self.assertTrue(route["estimated"])
        self.assertIn("haversine", route["method"])

    def test_rejects_unknown_mode(self):
        with self.assertRaises(ValueError):
            estimate_route([0, 0], [1, 1], "teleport")


if __name__ == "__main__":
    unittest.main()
