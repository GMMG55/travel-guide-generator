import copy
import unittest

from scripts.validate_guide import validate_guide


def valid_guide():
    return {
        "schema_version": "1.0",
        "meta": {
            "title": "测试攻略",
            "destination": "测试地",
            "language": "zh-CN",
            "start_date": "2026-09-20",
            "days": 1,
        },
        "preferences": {"pace": "balanced"},
        "sources": [
            {
                "id": "official",
                "title": "官方",
                "type": "official",
                "checked_at": "2026-09-01",
            }
        ],
        "days": [
            {
                "day": 1,
                "date": "2026-09-20",
                "title": "测试",
                "items": [
                    {
                        "name": "地点 A",
                        "start": "09:00",
                        "end": "10:00",
                        "source_ids": ["official"],
                    },
                    {
                        "name": "地点 B",
                        "start": "10:30",
                        "end": "11:30",
                        "route_from_previous": {
                            "duration_min": 20,
                            "estimated": True,
                            "method": "test",
                        },
                    },
                ],
            }
        ],
    }


class ValidateGuideTests(unittest.TestCase):
    def test_rejects_unknown_schema_version(self):
        guide = valid_guide()
        guide["schema_version"] = "9.9"

        report = validate_guide(guide)

        self.assertFalse(report["valid"])
        self.assertEqual(report["errors"][0]["code"], "SCHEMA_VERSION")

    def test_valid_guide_has_no_errors_or_conflicts(self):
        report = validate_guide(valid_guide())

        self.assertTrue(report["valid"])
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["conflicts"], [])

    def test_detects_overlap_and_insufficient_transit_time(self):
        guide = copy.deepcopy(valid_guide())
        second = guide["days"][0]["items"][1]
        second["start"] = "09:50"
        second["route_from_previous"]["duration_min"] = 30

        report = validate_guide(guide)
        codes = {item["code"] for item in report["conflicts"]}

        self.assertIn("TIME_OVERLAP", codes)
        self.assertIn("TRANSIT_TOO_SHORT", codes)

    def test_detects_outside_opening_hours(self):
        guide = copy.deepcopy(valid_guide())
        guide["days"][0]["items"][0]["opening_hours"] = {
            "open": "10:00",
            "close": "18:00",
        }

        report = validate_guide(guide)

        self.assertEqual(report["conflicts"][0]["code"], "OUTSIDE_OPENING_HOURS")


if __name__ == "__main__":
    unittest.main()
