# CS F301 Assignment 2 — Verification audit

Scope: four problem implementations, test harness, restricted Racket syntax,
requested runtime versions, repository integrity, and readiness for submission.

## Source and independent checks

- P1: exhaustive independent enumeration of `4!^3 = 13,824` candidates;
  3 solutions for the original 8 clues and exactly 1 for clues 1–9.
- P2: independent Python reference enumeration reproduced the 7 listed
  equations for `[4,2,5,3]`, the empty result for `[2,3,4]`, and the
  single result for `[2,4,8]`; additional repeated-number/zero cases checked.
- S1: the actual `.rkt` source forms were evaluated by a separate Python
  interpreter for the assignment's permitted Scheme subset; the documented
  balanced-tree case and 100 deterministic randomized trees matched reference
  traversal and height/leaf logic.
- S2: the actual `.rkt` source forms were checked in the same subset
  interpreter; all four documented examples and boundary conditions matched,
  as did 150 randomized nested-list cases and one 100-level nesting test.
- Built-in restrictions: the Racket source passed the checked-in forbidden-name
  static checks; sources start with `#lang racket/base` and have no top-level
  calls.
- Test discovery: supports the final GROUPID-prefixed filenames.

These checks are **not substitutes for real SWI-Prolog or Racket execution**.
The subset interpreter is a secondary logic check, not a certified Racket
implementation, and the randomized test counts refer only to that interpreter.

## Runtime state

The isolated authoring environment lacks both `swipl` and `racket`. An attempt
to update package indexes failed because its network DNS could not resolve the
package host. At this audit's conclusion, the Python unit test runner reported
`30 tests`, `5 passed`, `25 skipped` (the skipped ones require the language
runtimes). **Do not report these 30 as passed**.

The original project is recovered from the prior 31-commit Git bundle.
Additional review and harness improvements are committed separately. Before
submission, run one of:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\verify_windows.ps1 -InstallRuntimes
```

```bash
python3 -m unittest discover -s tests -v
```

The Windows runner requires SWI-Prolog 9.x and Racket 8.x and fails on test
skips; the Linux command should be run only after verifying both runtimes are
installed. GitHub Actions repeats the checks once the repository is pushed.

## Still required for a real submission

1. Supply the actual **group ID** and rename the four `code/id_q*` files.
2. Run all 30 tests under SWI-Prolog 9.x and Racket 8.x, including S2's
   10,000-element and 100-level stress tests. Repair any observed failures.
3. Configure an accessible GitHub remote and push the actual repository with
   history intact; verify CI passes. Do not submit only the ZIP.
4. Obtain genuine, distinct group-member contributions and commits where
   required; a shared Git identity is not evidence of every member's work.
5. Address the prompt decomposition marking risk: prior broad user requests
   were preserved accurately; granular commits do not retroactively create
   one-predicate-at-a-time AI prompts.
6. Prepare all members for the individual viva.

The group-ID details, remote URL, and individual group contributions were not
supplied when this audit was written. No GitHub push or real interpreter test
is claimed.
