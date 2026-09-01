import unittest

from scripts.search_guide import format_search_queries


class FormatSearchQueriesTests(unittest.TestCase):
    def test_returns_queries_for_requested_type(self):
        queries = format_search_queries("泰山", "food")

        self.assertEqual(len(queries), 4)
        self.assertTrue(all("泰山" in query for query in queries))
        self.assertIn("泰山美食推荐", queries)

    def test_unknown_type_falls_back_to_general(self):
        self.assertEqual(
            format_search_queries("泰山", "unknown"),
            format_search_queries("泰山", "general"),
        )


if __name__ == "__main__":
    unittest.main()
