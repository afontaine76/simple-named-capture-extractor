"""Extract named capture groups from a regex match into a dictionary.

Why this exists: Python's ``re`` module exposes named groups through
``Match.groupdict()``, but that returns ``None`` for groups that did not
participate in the match. Callers almost always want only the groups that
actually matched, and they want the values as plain strings. This module
provides that small transformation plus an ``all`` variant for repeated
matches.

The design choice: a group that did not participate is omitted from the
result rather than included with a ``None`` value. This keeps the dictionary
free of ``Optional[str]`` values and makes membership checks meaningful.
"""

from __future__ import annotations

import re
from typing import Dict, List, Pattern, Union

PatternType = Union[str, Pattern[str]]


def _compile(pattern: PatternType) -> Pattern[str]:
    """Return a compiled pattern, accepting either a string or a Pattern.

    Accepting both mirrors ``re.match`` and friends, so callers do not have to
    remember which form this helper wants.
    """
    if isinstance(pattern, str):
        return re.compile(pattern)
    if isinstance(pattern, re.Pattern):
        return pattern
    raise TypeError(
        "pattern must be a string or a compiled regular expression"
    )


def extract_named_groups(pattern: PatternType, text: str) -> Dict[str, str]:
    """Run *pattern* against *text* and return matched named groups.

    Returns a dictionary mapping each named group that participated in the
    match to its matched substring. Groups that did not participate are
    omitted. If the pattern does not match, an empty dictionary is returned.

    Raises ``TypeError`` if *pattern* is neither a string nor a compiled
    pattern, and ``re.error`` if a string pattern is invalid.
    """
    compiled = _compile(pattern)
    match = compiled.search(text)
    if match is None:
        return {}
    return {
        name: value
        for name, value in match.groupdict().items()
        if value is not None
    }


def extract_named_groups_all(pattern: PatternType, text: str) -> List[Dict[str, str]]:
    """Run *pattern* against *text* and return every match's named groups.

    Each element of the returned list is the dictionary produced by
    :func:`extract_named_groups` for one match, in the order the matches
    occur. An empty list is returned when there are no matches.
    """
    compiled = _compile(pattern)
    results: List[Dict[str, str]] = []
    for match in compiled.finditer(text):
        results.append({
            name: value
            for name, value in match.groupdict().items()
            if value is not None
        })
    return results
