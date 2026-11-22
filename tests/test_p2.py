"""P2: exact SWI-Prolog equation lists, empties and division edge cases."""
import pathlib
import shutil
import subprocess
import unittest

SOURCE = pathlib.Path(__file__).resolve().parents[1] / "code" / "id_q2.pl"
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

    def test_return_type_is_string(self):
        self.assertEqual(goal_output(
            "generate_equation([2,4,8],E),string(E),write(ok)"), 'ok')


if __name__ == '__main__':
    unittest.main()
