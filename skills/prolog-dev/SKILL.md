---
name: prolog-dev
description: Incrementally implement and check CS F301 Assignment 2 predicates in SWI-Prolog 9.x.
---

# Prolog development instructions

- Target **SWI-Prolog 9.x**. Use the exact required predicate names and arities.
- Work on **one predicate, one test file, or one review per AI prompt**. Preserve the actual prompt text; do not fabricate past prompts.
- Treat predicates declaratively: name variables for their logical meaning and document the relation they enforce.
- Favor ground, finite generation with explicit constraints; ensure `generate_equation/2` terminates on lists of length 0 and 1.
- Avoid `assert/1`, `retract/1`, and any global state; do not introduce initialization directives or `halt/0` calls.
- Respect permitted libraries: `lists`, `apply`, `yall`, `aggregate` (standard SWI built-ins are allowed).
- Avoid hardcoded puzzle answers. Check all active clue subsets with the same generator.
- For arithmetic, evaluate tree values directly, enforcing nonzero exact integer division **at every node**; never evaluate by parsing a generated string.
- For equations, obey the exact parentheses/precedence/associativity rules; return Prolog strings, not atoms.

## Running and testing

- `swipl -q -f code/id_q1.pl -g main -t halt`
- `swipl -q -f code/id_q1.pl -g "count_solutions([1,2,3,4,5,6,7,8],N),writeln(N)" -t halt`
- `swipl -q -f code/id_q2.pl -g "all_equations([4,2,5,3],E),writeln(E)" -t halt`
- Run `python3 tools/run_strict_tests.py` for the complete suite. To run the two Prolog test files only, use `python3 -m unittest discover -s tests -p 'test_p*.py' -v`.

## Self-review checklist

1. Exact name, arity, types and output format.
2. All stated examples, zero/empty, single-element, negative intermediate and repeated-number cases.
3. Finite generation and no unwanted output while loading.
4. No forbidden libraries, impure/global operations, hardcoded final answers, or evaluation-by-string.
5. Separate meaningful Git commits, accurate prompt record and no unsupported claims of executed tests.

## Known AI failure modes

- Unbound-variable negation appears to work but filters incorrectly.
- Assuming a puzzle is unique without counting all solutions.
- Accidentally generating duplicate outputs for distinct expression trees.
- Treating `/` as floating-point division or accepting inexact intermediate divisions.
- Incorrectly omitting parentheses on equal-precedence right children.
- Printing atoms instead of SWI-Prolog strings, or adding stray prompts/output.
