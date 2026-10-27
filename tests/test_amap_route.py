import io
import json
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from scripts import amap_route


class AmapRouteTests(unittest.TestCase):
    @patch("scripts.amap_route.urlopen")
    def test_request_json_uses_encoded_query_and_timeout(self, mock_urlopen):
        response = mock_urlopen.return_value.__enter__.return_value
        response.read.return_value = b'{"status":"1"}'

        result = amap_route.request_json(
            "https://restapi.amap.com/test",
            {"address": "青岛站", "output": "json"},
        )

        self.assertEqual(result, {"status": "1"})
        request_url = mock_urlopen.call_args.args[0]
        self.assertIn("address=%E9%9D%92%E5%B2%9B%E7%AB%99", request_url)
        self.assertEqual(mock_urlopen.call_args.kwargs["timeout"], 10)

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
