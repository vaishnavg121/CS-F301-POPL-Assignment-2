"""S1: Racket output against examples, empty/skewed/deep trees and static rules."""
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest

CODE_DIR = pathlib.Path(__file__).resolve().parents[1] / "code"
SOURCES = sorted(CODE_DIR.glob("*_q3.rkt"))
if len(SOURCES) != 1:
    raise RuntimeError(f"Expected one *_q3.rkt in {CODE_DIR}; found {SOURCES}")
SOURCE = SOURCES[0]
RACKET = shutil.which('racket')


def evaluate(*calls):
    # Submission files contain definitions only; emulate the grader in a temp file.
    with tempfile.TemporaryDirectory() as temp:
        file = pathlib.Path(temp) / 'submission-with-calls.rkt'
        file.write_text(SOURCE.read_text() + '\n' + '\n'.join(calls) + '\n')
        run = subprocess.run([RACKET, str(file)], capture_output=True,
                             text=True, timeout=45, check=False)
    if run.returncode:
        raise AssertionError(run.stderr)
    return run.stdout


class StaticS1Tests(unittest.TestCase):
    def test_language_and_restricted_primitives(self):
        src = SOURCE.read_text()
        self.assertTrue(src.startswith('#lang racket/base\n'))
        clean = '\n'.join(line.split(';', 1)[0] for line in src.splitlines())
        forbidden = ('append', 'reverse', 'length', 'map', 'filter', 'member',
                     'memq', 'set!', 'displayln', 'for', 'require', 'vector',
                     'hash', 'printf', 'eqv?', 'equal?')
        for name in forbidden:
            with self.subTest(name=name):
                self.assertIsNone(re.search(
                    rf'(?<![\w-]){re.escape(name)}(?![\w-])', clean))


@unittest.skipUnless(RACKET, 'Racket runtime not installed')
class RuntimeS1Tests(unittest.TestCase):
    def test_no_load_output(self):
        run = subprocess.run([RACKET, str(SOURCE)], capture_output=True,
                             text=True, timeout=20)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout, '')

    def test_complete_balanced_example(self):
        tree = "'(4 (2 (1 () ()) (3 () ())) (6 (5 () ()) (7 () ())))"
        self.assertEqual(evaluate(
            f'(print-inorder {tree})',
            f'(print-all-traversals {tree})',
            f'(print-height-and-leaves {tree})'),
            '(1 2 3 4 5 6 7)\n'
            '(1 2 3 4 5 6 7)\n'
            '(4 2 1 3 6 5 7)\n'
            '(1 3 2 5 7 6 4)\n'
            '(3 4)\n')

    def test_skewed_and_symbol_trees(self):
        self.assertEqual(evaluate(
            "(print-all-traversals '(1 () (2 () (3 () ()))))",
            "(print-height-and-leaves '(1 () (2 () (3 () ()))))"),
            '(1 2 3)\n(1 2 3)\n(3 2 1)\n(3 1)\n')
        self.assertEqual(evaluate(
            "(print-all-traversals '(a (b () ()) (c () ())))",
            "(print-height-and-leaves '(a (b () ()) (c () ())))"),
            '(b a c)\n(a b c)\n(b c a)\n(2 2)\n')

    def test_traversals_visit_left_subtree_first(self):
        # Instrument only the temporary grader driver. Output alone would also
        # match if a traversal recursively built the right subtree first.
        self.assertEqual(evaluate(
            '''(require racket/trace)
            (define visited '())
            (current-trace-notify void)
            (current-trace-print-args
             (lambda (_name args _keywords _keyword-values _depth)
               (when (pair? (car args))
                 (set! visited (cons (caar args) visited)))
               (newline)))
            (trace inorder-reversed preorder-reversed postorder-reversed)
            (print-all-traversals '(r (l (a () ()) ()) (q () (b () ()))))
            (displayln (reverse visited))'''),
            '(a l r q b)\n(r l a q b)\n(a l b q r)\n'
            '(r l a q b r l a q b r l a q b)\n')

    def test_single_node_and_left_skew(self):
        self.assertEqual(evaluate(
            "(print-all-traversals '(9 () ()))",
            "(print-height-and-leaves '(9 () ()))"),
            '(9)\n(9)\n(9)\n(1 1)\n')
        self.assertEqual(evaluate(
            "(print-all-traversals '(1 (2 (3 () ()) ()) ()))",
            "(print-height-and-leaves '(1 (2 (3 () ()) ()) ()))"),
            '(3 2 1)\n(1 2 3)\n(3 2 1)\n(3 1)\n')

    def test_empty_tree(self):
        self.assertEqual(evaluate(
            "(print-inorder '())",
            "(print-all-traversals '())",
            "(print-height-and-leaves '())"),
            '()\n()\n()\n()\n(0 0)\n')

    def test_deep_tree(self):
        tree = '(7 () ())'
        for i in range(1, 101):
            tree = f'({i} {tree} ())'
        self.assertEqual(evaluate(f"(print-height-and-leaves '{tree})"),
                         '(101 1)\n')


if __name__ == '__main__':
    unittest.main()
