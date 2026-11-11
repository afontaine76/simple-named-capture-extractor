import re
import unittest

from simple_named_capture_extractor import (
    extract_named_groups,
    extract_named_groups_all,
)


class ExtractNamedGroupsTests(unittest.TestCase):
    def test_simple_match(self):
        result = extract_named_groups(r"(?P<year>\d{4})-(?P<month>\d{2})", "2024-06")
        self.assertEqual(result, {"year": "2024", "month": "06"})

    def test_no_match_returns_empty_dict(self):
        result = extract_named_groups(r"(?P<year>\d{4})", "no digits here")
        self.assertEqual(result, {})

    def test_skips_groups_that_did_not_participate(self):
        # The optional group is absent, so it must not appear in the result.
        result = extract_named_groups(r"(?P<a>a)(?P<b>b)?", "a")
        self.assertEqual(result, {"a": "a"})
        self.assertNotIn("b", result)

    def test_optional_group_present(self):
        result = extract_named_groups(r"(?P<a>a)(?P<b>b)?", "ab")
        self.assertEqual(result, {"a": "a", "b": "b"})

    def test_unnamed_groups_are_ignored(self):
        result = extract_named_groups(r"(\d+)-(?P<word>\w+)", "42-answer")
        self.assertEqual(result, {"word": "answer"})

    def test_search_finds_match_anywhere(self):
        result = extract_named_groups(r"(?P<word>\w+)", "---hello---")
        self.assertEqual(result, {"word": "hello"})

    def test_accepts_compiled_pattern(self):
        pattern = re.compile(r"(?P<key>\w+)=(?P<value>\w+)")
        result = extract_named_groups(pattern, "x=1")
        self.assertEqual(result, {"key": "x", "value": "1"})

    def test_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            extract_named_groups(123, "text")

    def test_invalid_pattern_raises_re_error(self):
        with self.assertRaises(re.error):
            extract_named_groups(r"(?P<unclosed", "text")

    def test_empty_text_returns_empty_dict(self):
        result = extract_named_groups(r"(?P<x>\w+)", "")
        self.assertEqual(result, {})

    def test_empty_match_value_is_kept(self):
        # A group that matched the empty string is not the same as one that
        # did not participate, so it must be present with an empty value.
        result = extract_named_groups(r"(?P<x>a?)(?P<y>b)", "b")
        self.assertEqual(result, {"x": "", "y": "b"})


class ExtractNamedGroupsAllTests(unittest.TestCase):
    def test_multiple_matches(self):
        result = extract_named_groups_all(
            r"(?P<key>\w+)=(?P<value>\w+)", "a=1 b=2"
        )
        self.assertEqual(
            result,
            [
                {"key": "a", "value": "1"},
                {"key": "b", "value": "2"},
            ],
        )

    def test_no_matches_returns_empty_list(self):
        result = extract_named_groups_all(r"(?P<x>\d+)", "letters")
        self.assertEqual(result, [])

    def test_skips_non_participating_groups_per_match(self):
        result = extract_named_groups_all(r"(?P<a>a)(?P<b>b)?", "a ab")
        self.assertEqual(result, [{"a": "a"}, {"a": "a", "b": "b"}])

    def test_accepts_compiled_pattern(self):
        pattern = re.compile(r"(?P<n>\d+)")
        result = extract_named_groups_all(pattern, "1 22 333")
        self.assertEqual(result, [{"n": "1"}, {"n": "22"}, {"n": "333"}])

    def test_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            extract_named_groups_all(3.14, "text")


if __name__ == "__main__":
    unittest.main()
