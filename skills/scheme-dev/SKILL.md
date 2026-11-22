---
name: scheme-dev
description: Incrementally implement and review the restricted Racket Scheme parts of CS F301 Assignment 2.
---

# Scheme development instructions

- Target **Racket 8.x**, with **`#lang racket/base`** as the first line of each `.rkt` source.
- Each AI prompt targets only **one function, one test file, or one review**. Copy real prompts verbatim into the required `prompts/` records.
- Treat functions as pure structural recursion; pass all state through arguments. Prefer tail recursion when practical.
- Use only: `define`, `lambda`, `let`, `let*`, `letrec`, named `let`, `if`, `cond` with `else`, `and`, `or`, `not`, `begin`, `'`, `cons`, `car`, `cdr`, `list`, compositions of `car`/`cdr` to depth 4, `null?`, `pair?`, `eq?`, `assq`, `assoc`, `+`, `-`, `*`, `<`, `>`, `<=`, `>=`, `=`, `max`, `display`, `newline` (and `read` for S2 only).
- **Never** use `set!`, vectors, hashes, strings, `do`, `for`, `length`, `append`, `reverse`, `map`, `filter`, `member`, `memq`, `list-ref`, or `list-tail`. Write recursive helpers with approved built-ins.
- Output exactly the required list per line and end every printed result with `newline`.
- `print-*` functions must have no top-level invocations; the grader supplies function calls.
- S2 must compute each original list length **before** adding `x`, recurse into nested lists at every depth, and expose `my-length`, `my-map`, `make-inserter`, and exactly one final `insert-if-short` definition using `make-inserter`.

## Running and testing

- `racket code/id_q3.rkt`
- `racket code/id_q4.rkt`
- To run grader-style calls, **make a temporary copy** of the source and append the calls there; never leave top-level calls in the submission file.
- Test empty/leaf/skewed trees; empty nested lists; `n=0`; deep nesting (100); wide lists (10,000).

## Self-review checklist

1. Only permitted built-ins, exact function names and `#lang racket/base`.
2. No mutation or hidden state; correct recursion and order of traversal.
3. Every print function emits the exact lines and one ending newline.
4. Every nested list (including empty and top-level) is processed against original length.
5. Correct base cases and scaling on the specified hidden stress tests.
6. Match the actual prompts and scope of individual commits.

## Known AI failure modes

- Accidental use of `append`, `reverse`, `length`, `map`, `equal?`, `string?`, `zero?`, `displayln`, or other forbidden helpers.
- Printing values individually instead of a Scheme list.
- Comparing length after insertion, causing off-by-one errors.
- Skipping the outermost/empty list or flattening subtrees accidentally.
- Non-tail recursion that blows the stack or quadratic list construction on large cases.
