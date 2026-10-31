"""Elementary cellular automata: Wolfram's one-dimensional rules, 0 to 255."""

from __future__ import annotations

import random

__all__ = ["RULES", "decode_rule", "seed_row", "step", "run", "render"]

#: Every rule number Wolfram's scheme can express.
RULES = range(256)


def decode_rule(rule: int) -> list[int]:
    """Expand a Wolfram code into its eight-entry lookup table.

    Read the neighbourhood (left, centre, right) as a binary number -- 111 is
    7, 000 is 0 -- and the rule number's bits say what each one becomes.  So
    ``table[4 * left + 2 * centre + right]`` is the new state of the centre
    cell, which is why rule 30 is `00011110` in binary.
    """
    if not 0 <= rule <= 255:
        raise ValueError("rule must be between 0 and 255, got %r" % (rule,))
    return [(rule >> index) & 1 for index in range(8)]


def seed_row(width: int, *, seed: int | None = None, single: bool = False) -> list[int]:
    """The first generation: a lone cell, or random noise from *seed*."""
    if width < 1:
        raise ValueError("width must be at least 1")
    if single:
        row = [0] * width
        row[width // 2] = 1
        return row
    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    return [rng.getrandbits(1) for _ in range(width)]


def step(row: list[int], table: list[int]) -> list[int]:
    """One generation, wrapping around the ends -- the row lives on a torus."""
    width = len(row)
    if width == 0:
        raise ValueError("row must not be empty")
    out = [0] * width
    for index in range(width):
        neighbourhood = (
            (row[(index - 1) % width] << 2)
            | (row[index] << 1)
            | row[(index + 1) % width]
        )
        out[index] = table[neighbourhood & 7]
    return out


def run(
    rule: int,
    width: int = 79,
    generations: int = 40,
    *,
    seed: int | None = None,
    single: bool = False,
) -> list[list[int]]:
    """Evaluate *rule* for *generations* rows and return the whole history."""
    if generations < 1:
        raise ValueError("generations must be at least 1")
    table = decode_rule(rule)
    row = seed_row(width, seed=seed, single=single)
    rows = [row]
    for _ in range(generations - 1):
        row = step(row, table)
        rows.append(row)
    return rows


def render(rows: list[list[int]], *, on: str = "#", off: str = " ") -> list[str]:
    """Turn a history into lines of text."""
    return ["".join(on if cell else off for cell in row) for row in rows]
