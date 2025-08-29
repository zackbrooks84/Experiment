"""Test configuration helpers.

This module adjusts ``sys.path`` so that the package under test can be
imported when the test suite is invoked from arbitrary working directories.

Git Bash on Windows sometimes launches ``pytest`` from a different path than
expected, which means the repository root might not be on ``sys.path``.  Using
``pathlib`` to resolve the project root provides a robust, cross-platform
solution.
"""

from pathlib import Path
import sys

# Determine the absolute path to the repository root in a platform-agnostic
# way. ``Path.resolve`` handles any ``..`` segments and normalises the drive
# letter on Windows so comparisons succeed regardless of how the path was
# invoked.
ROOT = Path(__file__).resolve().parent.parent
ROOT_STR = str(ROOT)

# Prepend the resolved root to ``sys.path`` if it's not already present.  This
# allows ``import ai_identity`` to succeed even when tests are executed from
# outside the repository (e.g. from a Git Bash shell opened elsewhere).
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)

