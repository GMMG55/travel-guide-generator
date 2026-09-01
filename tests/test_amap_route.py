import io
import json
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from scripts import amap_route


class AmapRouteTests(unittest.TestCase):
    def test_get_amap_key_returns_none_when_unconfigured(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(amap_route.get_amap_key())

    def test_main_returns_structured_fallback_without_key(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        argv = [
            "amap_route.py",
            "--origin",
            "泰山站",
            "--destination",
            "红门",
            "--city",
            "泰安",
        ]

        with patch.dict(os.environ, {}, clear=True), patch.object(sys, "argv", argv):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as exit_context:
                    amap_route.main()

        result = json.loads(stdout.getvalue())
        self.assertEqual(exit_context.exception.code, 0)
        self.assertEqual(result["status"], "error")
        self.assertTrue(result["fallback"])
        self.assertIn("AMAP_KEY", result["message"])
        self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
