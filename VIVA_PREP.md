# CS F301 Assignment 2 — Individual viva preparation

The source files in `code/` are authoritative. These explanations help members demonstrate their own understanding; they do not replace individual study or actual contributions.

## P1: Prolog logic puzzle

**Representation.** Each solution is a four-element list of `p(Name,Dept,Lang,Project)`, with friends in Alex–Ben–Carla–Dana order. The language atom for C++ is quoted as `'c++'`, and the AI project atom is `'AI'`.

**How it works.** The three `permutation/2` goals generate independent one-to-one assignments of the four departments, four languages and four projects. That means every friend has a unique value for each attribute. Four friends have `4! = 24` possible assignments per attribute, so the generator checks `24 × 24 × 24 = 13,824` candidates before filtering.

Each `clue(N,Solution)` only checks a fully specified candidate. In `solution_for_clues(Active,Solution)`, `forall(member(N,Active),clue(N,Solution))` checks only selected clues, so omitting a clue genuinely relaxes the puzzle. `count_solutions/2` uses `findall/3`, then counts results using `length/2`.

**Why repair is necessary.** Clues 1–8 leave three candidates. Clue 9 states that the AI-project friend works in testing; it names no friend and is true of exactly one of those candidates. Repaired count is one.

**Backtracking.** Prolog can try another department permutation, then language permutation, then project permutation. `findall/3` collects all answers; `once/1` in `main/0` deliberately prints only one solution. `main/0` derives the answer instead of embedding a literal assignment.

**Likely viva questions.** What is a predicate? Why use `permutation` instead of choosing values independently? What is unification? What does `findall` do? Why can't we use `\=` to reject unbound fields safely? How does backtracking search work? What changes when `Active=[]`? Why is clue 9 independent of names?

## P2: Prolog arithmetic equations

**Tree representation.** A leaf is `num(N)` and a binary operator node is `op(Op,Left,Right)`. The generator recursively splits an input list into two nonempty consecutive pieces, so it never reorders or skips numbers. For each split it tries four binary operators.

**Safe integer division.** The `/` branch first rejects `RightValue=0` and requires `LeftValue mod RightValue = 0`. Only then is integer division `//` performed. This check is done recursively for **every** division node. Negative intermediate results are legal, because subtracting one integer from another is unrestricted.

**Formatting.** In `format_expression/2`, `+` and `-` have precedence 1, while `*` and `/` have precedence 2. A left child is parenthesized only when it has lower precedence; a right child is parenthesized when it has equal or lower precedence. This preserves unique trees: `1+2+3` means `(1+2)+3`, while `1+(2+3)` is a different tree and keeps its parentheses. Returned equations are SWI-Prolog **strings**, not atoms.

**Enumeration.** `generate_equation/2` chooses one nonempty split for the equals sign, constructs expressions on both sides, and requires their integer values to unify. `all_equations/2` uses `findall/3` and `sort/2`, removing duplicate strings and sorting by SWI term order. `count_equations/2` counts the final deduplicated list.

**Examples.** `[4,2,5,3]` produces exactly seven different equation strings; `[2,3,4]` produces none; `[2,4,8]` produces just `2*4=8`. For `[]` and `[3]`, no equals-sign split is possible, so generation fails normally. The problem permits multiple different equation strings that happen to evaluate to the same value.

**Likely viva questions.** Why is the recursion finite for a nonempty ground list? What are expression trees? What is the difference between precedence and associativity? Why do we parenthesize equal-precedence right operands? Why use `mod` before `//`? Why does `sort` remove duplicates? What is the role of backtracking?

## S1: Racket binary trees

**Representation.** An empty tree is `'()` and every node is `(value left right)`. Accessors are `car`, `cadr`, and `caddr` (all allowed). The three standard traversals are inorder `L,N,R`, preorder `N,L,R`, and postorder `L,R,N`.

**Accumulators.** Each `*-onto` helper returns traversal values prepended to an already computed suffix. This avoids `append` and `reverse`, which are forbidden. The traversal visits each node once, so it takes O(number of nodes) time and O(height) recursive-call depth plus result-list space.

**Height/leaves.** Empty tree has `(0 0)`. A leaf has `(1 1)`. For a nonempty tree, height is `1 + max(left-height,right-height)`; leaves are one for a node with two empty children, otherwise `left-leaves + right-leaves`. `tree-metrics` calculates both values together to avoid repeated traversal.

**Outputs.** `print-inorder` prints one complete list and newline; `print-all-traversals` prints three lists on three lines; `print-height-and-leaves` prints one `(height leaf-count)` list and newline. Definitions do not execute automatically when the source file is loaded.

**Likely viva questions.** What distinguishes traversal orders? What happens on the empty tree or a single node? Why are the helper calls positioned where they are? How do suffix lists avoid `append`? Why is a skewed tree's height equal to its node count?

## S2: Racket conditional nested insertion

**Original length.** Every list, including the outermost list and nested empty lists, is evaluated using its original top-level length. The `walk` function builds transformed children via `my-map`, then tests `(my-length lst)` on the **unmodified original**. If it passes, the original list's transformed elements are prefixed by `x`.

**List-versus-atom.** `pair?` identifies nonempty sublists, but it is false for empty `'()`; `null?` is therefore also necessary to recurse into nested empty lists. Ordinary atoms (digits or symbols) are kept unchanged.

**Higher-order function.** `make-inserter` receives `x` and a predicate `len-ok?` and returns a one-argument list transformer. `insert-if-short` is a specialization passing `(lambda (size) (< size n))`; only that final definition exists. `my-length` and `my-map` are defined locally instead of using forbidden built-ins; mapping and reversal are tail-recursive.

**Performance.** Over a nested-list structure of M total list elements, the recursive transformer processes each list element a constant number of times (including `my-length` and `my-map`), giving O(M) overall time and space for the result. Depth 100 is supported by recursive descent, and width 10,000 is handled by tail-recursive `my-map`/`my-reverse` and `my-length`.

**Input and output.** `print-insert-result` makes three `read` calls for `x`, `lst`, `n`, in that order; it uses `display` once on the result and `newline` once. There is no input prompt.

**Likely viva questions.** Why does `()` need special handling? What if `n=0`? What is the difference between `my-length` and `my-map`? How does the closure capture `x` and `len-ok?`? Why can't we use mutation or built-in `map`? How do original versus transformed lengths differ?

## Running the grader-style tests

The code files intentionally contain definitions only; read the top-level testing instructions in `README.md`. Execute the `tests/` files in an environment with SWI-Prolog 9.x and Racket 8.x. A Python test report with skipped interpreter-dependent tests is **not** evidence that the language code was executed successfully.
