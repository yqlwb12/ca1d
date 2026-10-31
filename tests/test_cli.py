"""Tests for the command line."""

import io
import unittest
from contextlib import redirect_stdout

from ca1d import cli


def run_cli(*argv):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = cli.main(list(argv))
    return code, buffer.getvalue()


class OutputTest(unittest.TestCase):
    def test_ascii_output_is_plain(self):
        code, out = run_cli("--ascii", "-r", "90", "--single", "-w", "9", "-n", "3")
        self.assertEqual(code, 0)
        self.assertNotIn("\x1b", out)
        self.assertEqual(out.splitlines(), ["....#....", "...#.#...", "..#...#.."])

    def test_generation_count(self):
        _, out = run_cli("--ascii", "-n", "7", "-w", "11")
        self.assertEqual(len(out.splitlines()), 7)

    def test_width_is_respected(self):
        _, out = run_cli("--ascii", "-n", "3", "-w", "13", "-s", "1")
        self.assertTrue(all(len(line) <= 13 for line in out.splitlines()))

    def test_show_rule_prints_the_table(self):
        code, out = run_cli("--show-rule", "-r", "30")
        self.assertEqual(code, 0)
        self.assertIn("111", out)
        self.assertIn("000", out)
        self.assertIn("1", out.splitlines()[-1])


class ArgumentTest(unittest.TestCase):
    def test_rule_out_of_range(self):
        with self.assertRaises(SystemExit) as caught:
            run_cli("-r", "256")
        self.assertEqual(caught.exception.code, 2)

    def test_zero_width(self):
        with self.assertRaises(SystemExit) as caught:
            run_cli("-w", "0")
        self.assertEqual(caught.exception.code, 2)

    def test_version(self):
        with self.assertRaises(SystemExit) as caught:
            run_cli("--version")
        self.assertEqual(caught.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
