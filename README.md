# CS F301 — Assignment 2: Logic and Functional Programming

A group repository for the four required programming-language problems. The group ID has not yet been supplied; before submitting, replace the `id` prefix in all four code filenames with your group ID, and use the group ID as the root repository/directory name.

## Required deliverables

- `code/id_q1.pl` — P1 department puzzle, clues 1–9, solving, solution count and output.
- `code/id_q2.pl` — P2 arithmetic expression generation, canonical formatting and equation enumeration/counting.
- `code/id_q3.rkt` — S1 inorder, all traversals, tree height and leaves.
- `code/id_q4.rkt` — S2 nested insertion, custom length/map, higher-order inserter, input/output.
- `tests/test_p1.py`, `tests/test_p2.py`, `tests/test_s1.py`, `tests/test_s2.py` — one test file per problem, including the assignment's examples and edge cases.
- `skills/prolog-dev/SKILL.md`, `skills/scheme-dev/SKILL.md` — reusable development/review skills.
- `prompts/P1.md`, `prompts/P2.md`, `prompts/S1.md`, `prompts/S2.md` — actual prompts, quoted verbatim, with separately identified implementation notes.
- `P1_REPORT.md` — original solution count and unique repair.

## Required environment and commands

Use **SWI-Prolog 9.x** and **Racket 8.x**. The assignment's grading commands use the group-ID-renamed files, for example:

```bash
swipl -q -f code/id_q1.pl -g main -t halt
swipl -q -f code/id_q1.pl -g "count_solutions([1,2,3,4,5,6,7,8],N),writeln(N)" -t halt
swipl -q -f code/id_q2.pl -g "all_equations([4,2,5,3],E),writeln(E)" -t halt
racket code/id_q3.rkt
racket code/id_q4.rkt
```

The two Racket commands load definitions only and intentionally print nothing. The grader appends its calls. To test a Scheme function, append a call to a **temporary copy** of the source file. To run all automated tests:

```bash
python3 -m unittest discover -s tests -v
```

The tests skip runtime assertions if either interpreter is missing. The GitHub Actions workflow now fails if either required runtime major version is absent or if any tests are skipped. Therefore a local run reporting `OK (skipped=...)` **does not** establish runtime correctness. The checked-in GitHub Actions workflow installs both runtimes before executing tests; CI cannot run until the repository is pushed to GitHub.

## Submission and collaboration checks

1. Replace `id` with the real group ID in all four code filenames; do not replace it with the student ID unless they are identical.
2. Preserve the incremental Git history and the actual prompts. The initial broad user request does not by itself demonstrate the assignment's one-predicate/function-per-prompt requirement; see `prompts/` for the accurate record.
3. Have each group member make their **own genuine contributions and commits** using their verified Git email. Do not retroactively ascribe another person's work to them.
4. After runtime tests pass, push the repository (not a ZIP) and verify the GitHub Actions test status.
5. Prepare for the individual viva. The grader assigns separate marks to understanding/ownership.

## Current verification note

The required local Prolog and Racket runtimes were unavailable in the authoring environment. Independent reference checks reproduced P1's solution counts (3 before repair, 1 after) and all three P2 equation examples. Static Scheme checks and source-parenthesis balance passed. The runtime tests must still execute in an actual SWI-Prolog 9.x/Racket 8.x installation or via GitHub Actions.

## Windows laptop validation

The project includes `tools/verify_windows.ps1`, which finds installed language
runtimes (also searching standard Program Files locations), verifies **SWI-Prolog
9.x** and **Racket 8.x**, and executes all tests. It fails if tests are skipped.

From Windows PowerShell in the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\verify_windows.ps1
```

If either runtime is absent, the optional `-InstallRuntimes` flag tries to
install an appropriate 9.x/8.x version through WinGet; if those versions are
not offered, install the exact required major versions from the official
archives and rerun:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\verify_windows.ps1 -InstallRuntimes
```

The runner writes `verification_windows.log` locally; the log is ignored by
Git. Python is required for the test harness. Tests discover the four source
files by suffix (`*_q1.pl`, `*_q2.pl`, `*_q3.rkt`, `*_q4.rkt`), so group-ID
renaming does not break them.

## Supplemental audit

See `TEST_AUDIT.md` for the exact completed checks and unresolved blockers.
The portable optional source-level reference checks can also run with Python:

```bash
python3 tools/offline_scheme_sim.py
python3 tools/randomized_audit.py
```

These secondary checks use a restricted Python evaluator rather than the
Racket executable and must never be reported as a Racket 8.x test pass.
