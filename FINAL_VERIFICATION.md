# CS F301 Assignment 2 — Final Verification

The six-page assignment handout was used to check the problem specifications, repository layout, and evaluation rubric.

| Verification | Result |
| --- | --- |
| Original Windows runs | Both passed **30 tests**, with **0 failures and 0 skips**, using SWI-Prolog 9.2.9 and Racket 8.18. |
| GitHub Actions before the review changes | All 30 tests passed on [the baseline commit](https://github.com/vaishnavg121/CS-F301-POPL-Assignment-2/actions/runs/45024444665). |
| GitHub Actions after the S1 and workflow fixes | All 30 tests passed with zero skips in [run 3](https://github.com/vaishnavg121/CS-F301-POPL-Assignment-2/actions/runs/45025921678). |
| Local final-review checks | P1 and P2 runtime suites and both Scheme static checks passed. The local Racket launch hit a Windows DLL relocation error. GitHub Actions supplied the complete native-runtime check. |

P1 has three assignments under clues 1–8 and one under clues 1–9. P2 reproduces the three prescribed equation sets. S1 visits left subtrees first and prints the required traversal and metrics lists. S2 uses each list's original top-level length and includes explicit tests for depth 100 and 10,000-element input.

The repository contains four source files, one test file per problem, both required skill files, four problem prompt records, and the P1 report. The prompt records retain the original requests and separately identify focused prompts actually issued during final review.

## Submission checks remaining

- Confirm the official group ID and apply it to the repository root name and the four source filenames.
- Confirm each student's Git contribution. The reviewed history contains commits attributed to Vaishnav. Chaitrali must make and own her own contributions for individual Git credit.
- Prepare both students for the individual viva. The new review prompts document the final review stages. The original implementation prompts retain their original scope.

See [README.md](README.md) for commands and [TEST_AUDIT.md](TEST_AUDIT.md) for coverage.

## Follow-up audit

The expanded suite passed all 31 tests with zero failures and zero skips using SWI-Prolog 9.2.9 and Racket CS 8.18. It adds coverage for selected-clue counting, nested division, left-first traversal call order and width-10,000 insertion boundaries. The published project and rubric items remain described above. See [TEST_AUDIT.md](TEST_AUDIT.md) for runtime details and the [Actions page](https://github.com/vaishnavg121/CS-F301-POPL-Assignment-2/actions) for the latest workflow result.
