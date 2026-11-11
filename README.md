# simple-named-capture-extractor

Runs a regex against text and returns a dictionary of named capture groups with their matches.

```python
from simple_named_capture_extractor import extract_named_groups, extract_named_groups_all

# One match anywhere in the text
result = extract_named_groups(r"(?P<year>\d{4})-(?P<month>\d{2})", "released 2024-06")
assert result == {"year": "2024", "month": "06"}

# Every match in the text
all_results = extract_named_groups_all(
    r"(?P<key>\w+)=(?P<value>\w+)", "a=1 b=2"
)
assert all_results == [
    {"key": "a", "value": "1"},
    {"key": "b", "value": "2"},
]
```

Both functions accept either a pattern string or a compiled `re.Pattern`.

## Why this exists

Python's `re` module already exposes named groups through `Match.groupdict()`,
but that dictionary includes every named group in the pattern, with `None` for
groups that did not participate in the match. Most callers want only the groups
that actually matched, and they want the values typed as `str` rather than
`Optional[str]`. This library performs that one transformation.

The trade-off: a group that did not participate is omitted from the result
instead of being included with a `None` value. That means you cannot
distinguish "group did not match" from "group is not in the pattern" by looking
at the dictionary alone. In exchange, every value in the dictionary is a real
string, and `if name in result` answers the question callers usually have.

## The awkward edge

A group that matched the empty string is kept, because it participated in the
match. For example, `extract_named_groups(r"(?P<x>a?)(?P<y>b)", "b")` returns
`{"x": "", "y": "b"}`. If you need to tell an empty match apart from a
non-participating group, use `re` directly.
