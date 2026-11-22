"""S2: nested insert outputs, higher-order callback, deep/wide stress tests."""
import pathlib
import re
import shutil
import subprocess
import tempfile
import unittest

SOURCE = pathlib.Path(__file__).resolve().parents[1] / 'code' / 'id_q4.rkt'
RACKET = shutil.which('racket')


def read_and_print(x, nested, limit, timeout=40):
    run = subprocess.run(
        [RACKET, str(SOURCE)], input='', capture_output=True,
        text=True, timeout=timeout, check=False,
    )
    if run.returncode:
        raise AssertionError(run.stderr)
    if run.stdout:
        raise AssertionError('submission file prints at load')
    with tempfile.TemporaryDirectory() as temp:
        path = pathlib.Path(temp) / 'driver.rkt'
        path.write_text(SOURCE.read_text() + '\n(print-insert-result)\n')
        run = subprocess.run(
            [RACKET, str(path)], input=f'{x}\n{nested}\n{limit}\n',
            capture_output=True, text=True, timeout=timeout, check=False,
        )
    if run.returncode:
        raise AssertionError(run.stderr)
    return run.stdout


def evaluate(expression):
    with tempfile.TemporaryDirectory() as temp:
        path = pathlib.Path(temp) / 'driver.rkt'
        path.write_text(SOURCE.read_text() + '\n(display ' + expression + ')\n(newline)\n')
        run = subprocess.run([RACKET, str(path)], capture_output=True,
                             text=True, timeout=40, check=False)
    if run.returncode:
        raise AssertionError(run.stderr)
    return run.stdout


class StaticS2Tests(unittest.TestCase):
    def test_no_banned_primitives(self):
        src = SOURCE.read_text()
        self.assertTrue(src.startswith('#lang racket/base\n'))
        code = '\n'.join(line.split(';', 1)[0] for line in src.splitlines())
        for name in ('append', 'reverse', 'length', 'map', 'filter',
                     'member', 'memq', 'set!', 'displayln', 'for', 'require',
                     'vector', 'hash', 'printf', 'eqv?', 'equal?'):
            with self.subTest(name=name):
                self.assertIsNone(re.search(rf'(?<![\w-]){re.escape(name)}(?![\w-])', code))
        self.assertEqual(len(re.findall(r'\(define \(insert-if-short\b', code)), 1)


@unittest.skipUnless(RACKET, 'Racket runtime not installed')
class RuntimeS2Tests(unittest.TestCase):
    def test_document_examples(self):
        examples = [
            ('42', '((1 2) (3 4 5) (6) ())', 3,
             '((42 1 2) (3 4 5) (42 6) (42))\n'),
            ('0', '(((1) 2) (3) ((4 5 6) ()))', 3,
             '((0 (0 1) 2) (0 3) (0 (4 5 6) (0)))\n'),
            ('7', '()', 3, '(7)\n'),
            ('7', '()', 0, '()\n'),
        ]
        for x, nested, n, expected in examples:
            with self.subTest(x=x, nested=nested, n=n):
                self.assertEqual(read_and_print(x, nested, n), expected)

    def test_custom_map_and_length(self):
        self.assertEqual(evaluate("(my-length '(7 8 9))"), '3\n')
        self.assertEqual(evaluate("(my-map (lambda (a) (* a 2)) '(1 2 3))"),
                         '(2 4 6)\n')

    def test_higher_order_len_predicate(self):
        self.assertEqual(evaluate(
            "((make-inserter 9 (lambda (len) (= len 0))) '(() (())))"),
            '((9) ((9)))\n')

    def test_nested_empty_lists_and_original_length(self):
        self.assertEqual(read_and_print('z', '((()) ())', 2),
                         '(((z)) (z))\n')

    def test_nesting_depth_one_hundred(self):
        nested = '()'
        expected = '(9)'
        for _ in range(100):
            nested = '(' + nested + ')'
            expected = '(9 ' + expected + ')'
        self.assertEqual(read_and_print('9', nested, 2), expected + '\n')

    def test_wide_list_ten_thousand_elements(self):
        nested = '(' + ' '.join(['1'] * 10000) + ')'
        self.assertEqual(read_and_print('9', nested, 2, timeout=65), nested + '\n')


if __name__ == '__main__':
    unittest.main()
