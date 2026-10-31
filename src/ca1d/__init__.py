"""ca1d -- elementary cellular automata in your terminal.

    >>> from ca1d import run
    >>> board = run(90, width=9, generations=3, single=True)
    >>> from ca1d import render
    >>> render(board, on="#", off=".")
    ['....#....', '...#.#...', '..#...#..']

One rule number, 0 to 255, and a row of cells.  That is the whole idea.
"""

from .core import RULES, decode_rule, render, run, seed_row, step

__version__ = "0.1.0"

__all__ = [
    "RULES",
    "__version__",
    "decode_rule",
    "render",
    "run",
    "seed_row",
    "step",
]
