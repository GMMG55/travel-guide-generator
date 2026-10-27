import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.package_skill import package_skill


class PackageSkillTests(unittest.TestCase):
    def test_extracted_package_builds_without_repository_files(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            output, _ = package_skill(root, temporary / "skill.zip")
            with ZipFile(output) as archive:
                names = archive.namelist()
                self.assertIn("travel-guide-generator/SKILL.md", names)
                self.assertIn("travel-guide-generator/assets/template.html", names)
                self.assertFalse(any("/.git/" in name or "/generated/" in name for name in names))
                self.assertFalse(any("/tests/" in name or "/screenshots/" in name for name in names))
                archive.extractall(temporary / "unpacked")
            installed = temporary / "unpacked" / "travel-guide-generator"
            process = subprocess.run(
                [sys.executable, "-B", str(installed / "scripts" / "build_guide.py"),
                 str(installed / "examples" / "sample-guide.json"),
                 "--output-base", str(temporary / "trip")],
                cwd=temporary, capture_output=True, text=True,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            for suffix in (".html", ".md", ".ics", ".geojson", ".normalized.json"):
                self.assertTrue((temporary / ("trip" + suffix)).is_file())

    def test_existing_archive_is_not_overwritten(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            output, _ = package_skill(root, Path(directory) / "skill.zip")
            original = output.read_bytes()
            with self.assertRaises(FileExistsError):
                package_skill(root, output)
            self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
