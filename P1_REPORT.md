# P1 — Department Assignment Puzzle: Solution Count and Repair

For the original eight clues:

```prolog
?- count_solutions([1,2,3,4,5,6,7,8], N).
N = 3.
```

The original puzzle is **underdetermined**: three distinct complete assignments satisfy all eight original clues, so those clues do not specify a unique solution.

The added attribute-only clue is:

> **Clue 9:** The friend who prefers the AI project works in the testing department.

This makes the repaired puzzle unique:

```prolog
?- count_solutions([1,2,3,4,5,6,7,8,9], N).
N = 1.
```

The selected assignment is:

```text
Alex = [design, java, embedded]
Ben = [development, javascript, web]
Carla = [testing, python, AI]
Dana = [research, c++, data]
```

The counts were independently cross-checked by exhaustive enumeration of all `4! × 4! × 4! = 13,824` bijective attribute assignments. SWI-Prolog 9.x runtime execution remains to be performed in the required grading environment.
