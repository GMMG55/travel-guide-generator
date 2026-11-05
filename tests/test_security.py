import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from scripts.amap_route import safe_error
from scripts.build_guide import build
from scripts.export_guide import export_all, ics_escape, ics_text
from scripts.guide_utils import load_json
from scripts.package_skill import RUNTIME_FILES, package_skill
from scripts.render_guide import render_file
from scripts.validate_guide import validate_guide


class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.guide = load_json(Path('examples/sample-guide.json'))

    def test_invalid_day_rejected_and_navigation_uses_safe_text(self):
        self.guide['days'][0]['day'] = '<img src=x onerror=alert(731)>'
        report = validate_guide(self.guide)
        self.assertFalse(report['valid'])
        self.assertIn('DAY_NUMBER', [error['code'] for error in report['errors']])
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'guide.html'
            render_file(self.guide, output, allow_invalid=True)
            html = output.read_text(encoding='utf-8')
            self.assertIn('label.textContent = s.label', html)
            self.assertNotIn("item.innerHTML =", html)

    def test_build_conflict_does_not_overwrite_any_output(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / 'guide'
            existing = base.with_suffix('.ics')
            existing.write_text('keep me', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                build(self.guide, base)
            self.assertEqual(existing.read_text(encoding='utf-8'), 'keep me')
            self.assertFalse(base.with_suffix('.html').exists())
            self.assertEqual(build(self.guide, base, force=True)['status'], 'ok')

    def test_direct_export_and_renderer_do_not_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / 'guide'
            base.with_suffix('.geojson').write_text('keep', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                export_all(self.guide, base)
            self.assertFalse(base.with_suffix('.md').exists())
            output = base.with_suffix('.html')
            output.write_text('keep', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                render_file(self.guide, output)
            self.assertEqual(output.read_text(encoding='utf-8'), 'keep')

    def test_secret_is_redacted_from_errors(self):
        self.assertNotIn('private-token', safe_error(Exception('request?key=private-token&x=1'), 'private-token'))

    def test_ics_newlines_and_timezone_cannot_inject_headers(self):
        self.assertNotIn('\r', ics_escape('text\r\nBEGIN:VEVENT'))
        self.guide['meta']['timezone'] = 'Asia/Shanghai\r\nBEGIN:VEVENT'
        with self.assertRaises(ValueError):
            ics_text(self.guide)

    def test_package_does_not_include_unlisted_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'
            for name in RUNTIME_FILES:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('test', encoding='utf-8')
            (root / 'assets' / 'credentials.json').write_text('secret', encoding='utf-8')
            output, _ = package_skill(root, Path(directory) / 'skill.zip')
            with ZipFile(output) as archive:
                self.assertNotIn('travel-guide-generator/assets/credentials.json', archive.namelist())


if __name__ == '__main__':
    unittest.main()
