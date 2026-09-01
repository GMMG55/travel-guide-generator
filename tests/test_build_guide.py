import tempfile
import unittest
from pathlib import Path

from scripts.build_guide import build
from scripts.guide_utils import load_json


class BuildGuideTests(unittest.TestCase):
    def test_sample_build_creates_all_export_formats(self):
        guide = load_json(Path("examples") / "sample-guide.json")

        with tempfile.TemporaryDirectory() as directory:
            output_base = Path(directory) / "guide"
            result = build(guide, output_base)

            self.assertEqual(result["status"], "ok")
            self.assertEqual(result["routes_estimated"], 2)
            self.assertEqual(len(result["files"]), 5)
            for output in result["files"]:
                self.assertTrue(Path(output).exists(), output)
            html = output_base.with_suffix(".html").read_text(encoding="utf-8")
            self.assertNotIn("{{", html)
            self.assertNotIn("行程质量检查", html)
            self.assertIn('class="edit-btn"', html)
            self.assertIn('class="item-edit-controls" hidden', html)
            self.assertIn('class="cost-editor item-edit-controls" hidden', html)
            self.assertIn("localStorage", html)

    def test_quality_section_only_appears_when_issues_exist(self):
        guide = load_json(Path("examples") / "sample-guide.json")
        guide["days"][0]["items"][1]["start"] = "08:31"

        with tempfile.TemporaryDirectory() as directory:
            output_base = Path(directory) / "guide"
            result = build(guide, output_base)

            self.assertEqual(result["status"], "ok")
            self.assertTrue(result["report"]["conflicts"])
            html = output_base.with_suffix(".html").read_text(encoding="utf-8")
            self.assertIn("行程质量检查", html)


if __name__ == "__main__":
    unittest.main()
