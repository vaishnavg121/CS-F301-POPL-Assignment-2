"""P1: compare printed solutions and finite clue counts with SWI-Prolog 9.x."""
import itertools
import pathlib
import shutil
import subprocess
import unittest

CODE_DIR = pathlib.Path(__file__).resolve().parents[1] / "code"
SOURCES = sorted(CODE_DIR.glob("*_q1.pl"))
if len(SOURCES) != 1:
    raise RuntimeError(f"Expected one *_q1.pl in {CODE_DIR}; found {SOURCES}")
SOURCE = SOURCES[0]
SWIPL = shutil.which("swipl")


def run_goal(goal):
    run = subprocess.run(
        [SWIPL, "-q", "-f", str(SOURCE), "-g", goal, "-t", "halt"],
        capture_output=True, text=True, timeout=45, check=False,
    )
    if run.returncode:
        raise AssertionError(f"Goal {goal!r} failed: {run.stderr}")
    return run.stdout


class ReferenceP1Tests(unittest.TestCase):
    def test_original_three_and_repaired_unique(self):
        departments = ('research', 'development', 'design', 'testing')
        languages = ('python', 'java', 'c++', 'javascript')
        projects = ('AI', 'web', 'embedded', 'data')
        found = []
        for deps in itertools.permutations(departments):
            for langs in itertools.permutations(languages):
                for projs in itertools.permutations(projects):
                    entries = dict(zip(('Alex', 'Ben', 'Carla', 'Dana'),
                                       zip(deps, langs, projs)))
                    ai = next(name for name in entries if entries[name][2] == 'AI')
                    data = next(name for name in entries if entries[name][2] == 'data')
                    testing = next(name for name in entries if entries[name][0] == 'testing')
                    design = next(name for name in entries if entries[name][0] == 'design')
                    if not all((
                        entries[ai][0] != 'research' and ai != 'Dana',
                        deps[0] != 'development' and langs[0] != 'c++',
                        entries[testing][1] == 'python',
                        projs[1] == 'web' and deps[1] != 'testing',
                        entries[design][1] == 'java',
                        projs[2] != 'embedded' and deps[2] != 'development',
                        langs[3] != 'java' and deps[3] in ('research', 'testing'),
                        entries[data][0] == 'research' and entries[data][1] != 'javascript',
                    )):
                        continue
                    found.append(entries)
        self.assertEqual(len(found), 3)
        kept = [e for e in found if e[next(k for k in e if e[k][2] == 'AI')][0] == 'testing']
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept[0], {
            'Alex': ('design', 'java', 'embedded'),
            'Ben': ('development', 'javascript', 'web'),
            'Carla': ('testing', 'python', 'AI'),
            'Dana': ('research', 'c++', 'data'),
        })


@unittest.skipUnless(SWIPL, "SWI-Prolog runtime not installed")
class RuntimeP1Tests(unittest.TestCase):
    def test_main_exact_output(self):
        self.assertEqual(run_goal("main"),
            "Alex = [design, java, embedded]\n"
            "Ben = [development, javascript, web]\n"
            "Carla = [testing, python, AI]\n"
            "Dana = [research, c++, data]\n")

    def test_solution_counts(self):
        for clues, expected in (
            ('[]', '13824'),
            ('[2,8]', '1440'),
            ('[2,8,8]', '1440'),
            ('[1,2,3,4,5,6,7,8]', '3'),
            ('[1,2,3,4,5,6,7,8,9]', '1'),
        ):
            with self.subTest(clues=clues):
                self.assertEqual(run_goal(
                    f"count_solutions({clues},N),format('~d',[N])"), expected)

    def test_each_clue_true_for_repaired_solution(self):
        self.assertEqual(run_goal(
            "solution_for_clues([1,2,3,4,5,6,7,8,9],S),"
            "forall(between(1,9,N),clue(N,S)),write(ok)"), 'ok')


if __name__ == '__main__':
    unittest.main()
