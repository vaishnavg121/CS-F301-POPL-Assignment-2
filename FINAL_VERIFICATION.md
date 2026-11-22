# CS F301 Assignment 2 — final handoff and verification checklist

**Status: code and independent checks completed; required SWI-Prolog and Racket runtime tests NOT yet executed.** Do not call the submission fully verified until the strict runner reports all tests passing with zero skips.

## Code covered

- **P1:** 9 clues, `solution_for_clues/2`, `count_solutions/2`, `main/0`; independent enumeration shows 3 assignments for original clues 1–8 and 1 assignment after clue 9.
- **P2:** ordered arithmetic expression trees, exact nonzero integer division, canonical parentheses, generation and distinct sorted enumeration; independent reference matches all published examples.
- **S1:** inorder/preorder/postorder printing; height and leaf count; empty, balanced, skewed, symbols and randomized trees checked in a restricted Scheme source evaluator.
- **S2:** custom `my-length`, `my-map`, higher-order `make-inserter`, `insert-if-short`, input reader; published examples plus randomized cases and 100-deep nesting checked in a restricted Scheme source evaluator.

These independent checks are supplementary. The required runtime tests have **not** yet been observed passing.

## Run on Windows (PowerShell)

1. Extract this project or clone the attached Git bundle; open PowerShell in the folder containing `code`, `tests`, and `tools`.
2. Run:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\tools\verify_windows.ps1 -InstallRuntimes
   ```

3. If WinGet cannot install the specific versions, install SWI-Prolog **9.x** and Racket **8.x** from their official distributions, then rerun without `-InstallRuntimes`.
4. The command must finish with **`PASS: all assignment tests executed without failures or skips.`** and produce `verification_windows.log`. If it exits nonzero, the implementation is not verified; inspect the printed failure and log.

Alternative with both interpreters already installed and on PATH:

```powershell
py -3 tools\run_strict_tests.py
```

The strict runner currently discovers **30 tests**; it deliberately fails when the required interpreters are unavailable, including if other tests passed.

## Mandatory pre-submission items

1. Replace `id` in `code/id_q1.pl`, `code/id_q2.pl`, `code/id_q3.rkt`, `code/id_q4.rkt` with the **actual group ID**, not an assumed individual student ID. Use group ID as repository/root name.
2. Verify `swipl -q -f code/GROUPID_q1.pl -g main -t halt` prints exactly four lines, and run the equivalent P2 and Scheme commands described in the assignment/README. Ensure Racket files emit no output when merely loaded.
3. Preserve the Git commit history. Push the **repository**, not just a ZIP, from a GitHub account with access to the intended group repository. Check CI is green and that tests were not skipped.
4. Ensure each group member has genuine, attributable commits and can explain their work during the viva. Never add fictitious contributions.
5. Preserve accurate verbatim AI prompt logs. Some initial user requests were broad and may not meet the assignment's strict one-function/predicate-per-prompt rule; the existing commits do not cure that record retroactively.

## Audit limitations

- No direct control of the user's Windows laptop from this chat.
- This container has no SWI-Prolog or Racket executable, and external package download/DNS failed; therefore 25 interpreter-dependent tests were unavailable.
- The original final GitHub repository URL, group ID, and membership have not been supplied.
- Neither remote GitHub push nor GitHub Actions has been performed here.

**Don't claim full marks are guaranteed.** Complete the runtime and GitHub checks before the official deadline.
