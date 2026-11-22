# CS F301 Principles of Programming Languages — Assignment 2

**Logic and Functional Programming** · BITS Pilani, Hyderabad Campus

| Group member | Institute ID |
| --- | --- |
| Venkatanaga Vaishnav Gadamsetty | 2024A7PS0026H |
| Chaitrali Dharmadhikari | 2024A7PS0133H |

This assignment uses Prolog for constraint solving and equation enumeration, and Scheme for recursive traversal and transformation.

| Problem | Implementation |
| --- | --- |
| **P1 — Department Assignment Puzzle, Reloaded** | Generates complete assignments and filters them by numbered clues. The original eight clues allow three solutions. An attribute-only ninth clue leaves one. |
| **P2 — Form a Valid Arithmetic Equation** | Enumerates expressions over consecutive input numbers, checks exact integer division, and returns distinct, sorted equation strings with canonical parentheses. |
| **S1 — Binary Tree Traversals** | Prints inorder, preorder, and postorder traversals and computes tree height and leaf count. |
| **S2 — Conditionally Insert into a Nested List** | Builds a higher-order inserter that checks the original length of each list, including the outermost list and empty lists. |

## Repository layout

| Path | Contents |
| --- | --- |
| [code/](code/) | Four source files, `id_q1.pl` through `id_q4.rkt` |
| [tests/](tests/) | One test file per problem |
| [skills/](skills/) | Prolog and Scheme development instructions |
| [prompts/](prompts/) | Verbatim AI requests and review outcomes, organized by problem |
| [P1_REPORT.md](P1_REPORT.md) | P1 solution count and ninth-clue repair |
| [tools/](tools/) and [.github/workflows/](.github/workflows/) | Test runners and GitHub Actions workflow |

## Run the programs

Use **SWI-Prolog 9.x** and **Racket 8.x**. The test harness requires **Python 3**. Run these commands from the repository root.

```text
swipl -q -f code/id_q1.pl -g main -t halt
swipl -q -f code/id_q2.pl -g "all_equations([4,2,5,3],E),writeln(E)" -t halt
racket code/id_q3.rkt
racket code/id_q4.rkt
```

The Racket files load silently. The grader appends function calls. To try the S1 and S2 entry points locally, append a call to a temporary copy of each source. For example, in PowerShell:

```powershell
$samples = New-Item -ItemType Directory -Path ([IO.Path]::Combine([IO.Path]::GetTempPath(), [guid]::NewGuid().ToString()))
$s1 = Join-Path $samples.FullName 's1.rkt'
$s2 = Join-Path $samples.FullName 's2.rkt'
Copy-Item code/id_q3.rkt $s1
Copy-Item code/id_q4.rkt $s2
Add-Content -Encoding ascii $s1 "`n(print-all-traversals '(1 () (2 () ())))"
Add-Content -Encoding ascii $s2 "`n(print-insert-result)"
racket $s1
'42 ((1 2) (3 4 5) (6) ()) 3' | racket $s2
```

## Run the tests

With both language runtimes on your PATH, run `python3 tools/run_strict_tests.py` or `py -3 tools/run_strict_tests.py` on Windows. The Windows verification script also locates the interpreters and checks their major versions.

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\verify_windows.ps1
```

The strict suite passed **30 tests with zero failures and zero skips** on Windows using SWI-Prolog 9.2.9 and Racket 8.18. GitHub Actions also passed the full suite. See [FINAL_VERIFICATION.md](FINAL_VERIFICATION.md) for run details.

## Before submission

Confirm the official Assignment 1 group ID and use it for the repository root name and the four source filename prefixes. Each student needs genuine, individually attributable Git contributions and must prepare for the individual viva.
