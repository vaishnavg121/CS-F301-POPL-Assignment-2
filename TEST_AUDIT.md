# CS F301 Assignment 2 — Test Audit

| Problem | Automated and focused checks |
| --- | --- |
| **P1** | Exact four-line output, individual clue truth values, and solution counts with no clues, the original eight clues, and all nine. Exhaustive enumeration checked all 13,824 complete assignments. Focused SWI-Prolog checks confirmed that reordering or repeating active clues leaves the counts unchanged. |
| **P2** | Exact equation lists for the three handout examples, string type, canonical parentheses, sorted and unique results, repeated operands, and empty and singleton inputs. Focused SWI-Prolog checks covered signed intermediate values, exact and inexact nested division, and zero divisors. |
| **S1** | Exact traversal and metrics output for empty, balanced, singleton, and skewed trees, including a depth-101 tree. The suite checks that loading is silent and checks the restricted Scheme primitives. A targeted trace in the supplemental evaluator verified that all three revised traversal helpers recurse into the left subtree first. |
| **S2** | All four handout examples, strict thresholds, original lengths, nested empty lists, higher-order callbacks, depth 100, and a list of 10,000 elements. The suite checks silent loading and the restricted Scheme primitives. |

## Runtime evidence

The two original Windows runs each passed all 30 tests with zero skips in SWI-Prolog 9.2.9 and Racket 8.18. During final review, the local Prolog suites and Scheme static checks passed. Windows prevented the Racket executable from launching in the review environment with `WinError 623` (illegal DLL relocation). The full post-fix runtime result was verified in [GitHub Actions](https://github.com/vaishnavg121/CS-F301-POPL-Assignment-2/actions/runs/45025921678).

## Supplemental checks

`python3 tools/offline_scheme_sim.py` evaluates the source in a restricted Python Scheme evaluator. `python3 tools/randomized_audit.py` compares that evaluator's results with independent reference logic on 100 trees, 150 nested lists, and one 100-level nested list. These are source-level checks. The GitHub Actions and Windows results report native interpreter runs.

The strict runner exits nonzero on test failure, interpreter error, any skipped test, or discovery of fewer than 30 tests. File discovery matches the four assignment suffixes, so replacing the `id_` prefixes with the official group ID preserves test discovery.
