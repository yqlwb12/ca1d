"""Tests for the automaton itself."""

import unittest

from ca1d.core import decode_rule, render, run, seed_row, step


class DecodeRuleTest(unittest.TestCase):
    def test_rule_30_is_the_famous_table(self):
        # Wolfram's rule 30, indexed 000..111:
        # 000->0 001->1 010->1 011->1 100->1 101->0 110->0 111->0
        self.assertEqual(decode_rule(30), [0, 1, 1, 1, 1, 0, 0, 0])

    def test_rule_204_copies_the_centre_cell(self):
        table = decode_rule(204)
        for neighbourhood in range(8):
            self.assertEqual(table[neighbourhood], (neighbourhood >> 1) & 1)

    def test_rule_51_inverts_the_centre_cell(self):
        table = decode_rule(51)
        for neighbourhood in range(8):
            self.assertEqual(table[neighbourhood], 1 - ((neighbourhood >> 1) & 1))

    def test_rule_0_and_255_are_the_extremes(self):
        self.assertEqual(decode_rule(0), [0] * 8)
        self.assertEqual(decode_rule(255), [1] * 8)

    def test_rejects_numbers_outside_a_byte(self):
        for bad in (-1, 256, 1000):
            with self.assertRaises(ValueError):
                decode_rule(bad)


class StepTest(unittest.TestCase):
    def test_rule_90_draws_a_sierpinski_gasket(self):
        board = run(90, width=9, generations=3, single=True)
        self.assertEqual(render(board, on="#", off="."), [
            "....#....",
            "...#.#...",
            "..#...#..",
        ])

    def test_rule_204_is_identity(self):
        row = [1, 0, 1, 1, 0, 0, 1]
        self.assertEqual(step(row, decode_rule(204)), row)

    def test_rule_51_is_the_complement(self):
        row = [1, 0, 1, 1, 0, 0, 1]
        self.assertEqual(step(row, decode_rule(51)), [1 - cell for cell in row])

    def test_rule_0_dies_out(self):
        self.assertEqual(step([1] * 6, decode_rule(0)), [0] * 6)

    def test_rule_255_fills_in(self):
        self.assertEqual(step([0] * 6, decode_rule(255)), [1] * 6)

    def test_the_row_wraps_around(self):
        # Under rule 64, 110 -> 1, and the left neighbour of cell 0 is the
        # last cell, so wrapping is the only way cell 0 can light up.
        self.assertEqual(step([1, 0, 1], decode_rule(64))[0], 1)

    def test_step_does_not_mutate_its_input(self):
        row = [1, 0, 0, 1]
        snapshot = list(row)
        step(row, decode_rule(110))
        self.assertEqual(row, snapshot)

    def test_empty_row_is_rejected(self):
        with self.assertRaises(ValueError):
            step([], decode_rule(30))


class RunTest(unittest.TestCase):
    def test_row_count_and_width(self):
        board = run(30, width=31, generations=12, seed=1)
        self.assertEqual(len(board), 12)
        self.assertTrue(all(len(row) == 31 for row in board))

    def test_first_row_is_the_seed(self):
        board = run(110, width=11, generations=4, seed=7)
        self.assertEqual(board[0], seed_row(11, seed=7))

    def test_same_seed_same_board(self):
        self.assertEqual(
            run(45, width=21, generations=10, seed=3),
            run(45, width=21, generations=10, seed=3),
        )

    def test_different_seeds_different_boards(self):
        self.assertNotEqual(
            run(45, width=21, generations=10, seed=3),
            run(45, width=21, generations=10, seed=4),
        )

    def test_single_seeds_the_middle_cell(self):
        board = run(30, width=7, generations=1, single=True)
        self.assertEqual(board[0], [0, 0, 0, 1, 0, 0, 0])

    def test_bad_dimensions(self):
        with self.assertRaises(ValueError):
            run(30, width=0, generations=5)
        with self.assertRaises(ValueError):
            run(30, width=5, generations=0)


class RenderTest(unittest.TestCase):
    def test_render_maps_bits_to_characters(self):
        self.assertEqual(render([[1, 0, 1]], on="#", off="."), ["#.#"])

    def test_render_keeps_the_full_width(self):
        for row in render([[0, 1, 0, 1]], on="#", off="."):
            self.assertEqual(len(row), 4)


if __name__ == "__main__":
    unittest.main()
