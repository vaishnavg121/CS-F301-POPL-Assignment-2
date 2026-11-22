"""P2: exact SWI-Prolog equation lists, empties and division edge cases."""
import pathlib
import itertools
from functools import lru_cache
import shutil
import subprocess
import unittest

CODE_DIR = pathlib.Path(__file__).resolve().parents[1] / "code"
SOURCES = sorted(CODE_DIR.glob("*_q2.pl"))
if len(SOURCES) != 1:
    raise RuntimeError(f"Expected one *_q2.pl in {CODE_DIR}; found {SOURCES}")
SOURCE = SOURCES[0]
SWIPL = shutil.which("swipl")


def goal_output(goal):
    run = subprocess.run(
        [SWIPL, '-q', '-f', str(SOURCE), '-g', goal, '-t', 'halt'],
        capture_output=True, text=True, timeout=50, check=False,
    )
    if run.returncode:
        raise AssertionError(f"Goal {goal!r} failed: {run.stderr}")
    return run.stdout


def all_equations(numbers):
    goal = (f"all_equations({numbers},Es),"
            "forall(member(E,Es),format('~s~n',[E]))")
    return goal_output(goal).splitlines()


def precedence(operator):
    return 2 if operator in ("*", "/") else 1


def print_reference_tree(tree):
    if len(tree) == 1:
        return str(tree[0])
    op, left, right = tree
    a, b = print_reference_tree(left), print_reference_tree(right)
    if len(left) > 1 and precedence(left[0]) < precedence(op):
        a = "(" + a + ")"
    if len(right) > 1 and precedence(right[0]) <= precedence(op):
        b = "(" + b + ")"
    return a + op + b


@lru_cache(maxsize=None)
def reference_expressions(numbers):
    if len(numbers) == 1:
        return [((numbers[0],), numbers[0])]
    results = []
    for cut in range(1, len(numbers)):
        for (left, a), (right, b) in itertools.product(
                reference_expressions(numbers[:cut]),
                reference_expressions(numbers[cut:])):
            for op in ("+", "-", "*", "/"):
                if op == "+":
                    value = a + b
                elif op == "-":
                    value = a - b
                elif op == "*":
                    value = a * b
                else:
                    if b == 0 or a % b:
                        continue
                    value = a // b
                results.append(((op, left, right), value))
    return results


def reference_equations(numbers):
    output = []
    for cut in range(1, len(numbers)):
        left = reference_expressions(tuple(numbers[:cut]))
        right = reference_expressions(tuple(numbers[cut:]))
        rights_by_value = {}
        for tree, value in right:
            rights_by_value.setdefault(value, []).append(tree)
        for tree, value in left:
            for equal_tree in rights_by_value.get(value, []):
                output.append(print_reference_tree(tree) + "=" +
                              print_reference_tree(equal_tree))
    return sorted(set(output))


class ReferenceP2Tests(unittest.TestCase):
    def test_reference_equation_examples(self):
        self.assertEqual(reference_equations([4, 2, 5, 3]), [
            '4*2-5=3', '4*2=5+3', '4-2=5-3', '4/2=5-3',
            '4=2*(5-3)', '4=2+(5-3)', '4=2+5-3',
        ])
        self.assertEqual(reference_equations([2, 3, 4]), [])
        self.assertEqual(reference_equations([2, 4, 8]), ['2*4=8'])
        self.assertEqual(reference_equations([0, 0]), ['0=0'])

    def test_reference_additional_edge_cases(self):
        # Independent exhaustive reference: repeated numbers, zero and mixed operators.
        for numbers in ([0, 0], [1, 1, 1], [1, 2, 0, 0],
                        [2, 2, 2, 2], [1, 2, 3, 4], [6, 3, 2]):
            with self.subTest(numbers=numbers):
                expected = reference_equations(tuple(numbers))
                self.assertEqual(expected, sorted(set(expected)))
                self.assertTrue(all(isinstance(e, str) and e.count('=') == 1
                                    for e in expected))



@unittest.skipUnless(SWIPL, 'SWI-Prolog runtime not installed')
class RuntimeP2Tests(unittest.TestCase):
    def test_assignment_example_seven(self):
        self.assertEqual(all_equations([4, 2, 5, 3]), [
            '4*2-5=3', '4*2=5+3', '4-2=5-3', '4/2=5-3',
            '4=2*(5-3)', '4=2+(5-3)', '4=2+5-3',
        ])

    def test_no_equation(self):
        self.assertEqual(all_equations([2, 3, 4]), [])

    def test_unique_equation(self):
        self.assertEqual(all_equations([2, 4, 8]), ['2*4=8'])

    def test_empty_singleton(self):
        self.assertEqual(all_equations([]), [])
        self.assertEqual(all_equations([3]), [])
        self.assertEqual(goal_output(
            'generate_equation([],_) -> write(unexpected) ; write(failed)'), 'failed')
        self.assertEqual(goal_output(
            'generate_equation([3],_) -> write(unexpected) ; write(failed)'), 'failed')

    def test_zero_and_exact_division(self):
        self.assertEqual(all_equations([0, 0]), ['0=0'])
        self.assertTrue(all('/' not in e for e in all_equations([0, 0, 0])))
        self.assertIn('6/3=2', all_equations([6, 3, 2]))
        self.assertIn('6=3*2', all_equations([6, 3, 2]))

    def test_count_agrees_with_list(self):
        for numbers in ([4, 2, 5, 3], [2, 3, 4], [0, 0], [6, 3, 2]):
            with self.subTest(numbers=numbers):
                self.assertEqual(int(goal_output(
                    f'count_equations({numbers},N),format("~d",[N])')),
                    len(all_equations(numbers)))

    def test_equation_set_matches_independent_reference(self):
        for numbers in ([0, 0], [1, 1, 1], [1, 2, 0, 0],
                        [2, 2, 2, 2], [1, 2, 3, 4], [6, 3, 2]):
            with self.subTest(numbers=numbers):
                self.assertEqual(all_equations(numbers),
                                 reference_equations(tuple(numbers)))

    def test_canonical_formatter_tree_structure(self):
        cases = [
            ("op('*',op('+',num(4),num(2)),num(3))", '(4+2)*3'),
            ("op('*',op('/',num(8),num(4)),num(2))", '8/4*2'),
            ("op('/',num(8),op('*',num(4),num(2)))", '8/(4*2)'),
            ("op('-',op('-',num(1),num(2)),num(3))", '1-2-3'),
            ("op('-',num(1),op('-',num(2),num(3)))", '1-(2-3)'),
            ("op('+',num(1),op('+',num(2),num(3)))", '1+(2+3)'),
            ("op('+',op('+',num(1),num(2)),num(3))", '1+2+3'),
            ("op('+',num(1),op('*',num(2),num(3)))", '1+2*3'),
        ]
        for tree, expected in cases:
            with self.subTest(tree=tree):
                self.assertEqual(goal_output(
                    f"format_expression({tree},S),format('~s',[S])"), expected)

    def test_return_type_is_string(self):
        self.assertEqual(goal_output(
            "generate_equation([2,4,8],E),string(E),write(ok)"), 'ok')


if __name__ == '__main__':
    unittest.main()
