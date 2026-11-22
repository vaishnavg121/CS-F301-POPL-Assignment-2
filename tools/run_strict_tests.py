"""Run all four assignment test files; never accept skipped interpreter tests.

Unlike a bare `python -m unittest discover`, this exits nonzero when SWI-Prolog
or Racket is absent even if the remaining static/reference tests pass.
"""

from pathlib import Path
import sys
import unittest


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    suite = unittest.defaultTestLoader.discover(
        start_dir=str(root / "tests"), pattern="test_*.py"
    )
    count = suite.countTestCases()
    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
    result = runner.run(suite)
    if count < 30:
        print(f"FAIL: expected at least 30 assignment tests; discovered {count}")
        return 1
    if result.skipped:
        print(
            f"FAIL: {len(result.skipped)} test(s) skipped. Install SWI-Prolog "
            "9.x and Racket 8.x; rerun before submitting."
        )
        return 1
    if not result.wasSuccessful():
        print("FAIL: one or more assignment checks failed.")
        return 1
    print(f"PASS: all {count} assignment tests executed successfully; no skips.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
