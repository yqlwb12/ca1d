"""Command line front end for ca1d."""

from __future__ import annotations

import argparse
import colorsys
import sys

from .core import RULES, decode_rule, render, run

__version__ = "0.1.0"

BLOCK = "\u2588"  # a full block, for terminals that can take it
SHADE = "\u00b7"


def _paint(text: str, rgb: tuple[int, int, int]) -> str:
    return "\x1b[38;2;%d;%d;%dm%s\x1b[0m" % (rgb[0], rgb[1], rgb[2], text)


def _row_colour(index: int, total: int) -> tuple[int, int, int]:
    """Cool-to-warm ramp: blue at the top, amber at the bottom."""
    hue = 0.58 - 0.46 * (index / max(1, total - 1))
    r, g, b = colorsys.hsv_to_rgb(hue % 1.0, 0.55, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)


def _show_rule(rule: int) -> str:
    table = decode_rule(rule)
    # Wolfram prints the table from 111 down to 000.
    header = " ".join(format(n, "03b") for n in range(7, -1, -1))
    body = " ".join("%3d" % table[n] for n in range(7, -1, -1))
    return "%s\n%s" % (header, body)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ca1d",
        description="Elementary cellular automata: Wolfram's rules, one row at a time.",
        epilog="examples:\n  ca1d\n  ca1d -r 110 -n 60 -w 120\n  ca1d -r 90 --single --color",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-r", "--rule", type=int, default=30, metavar="0-255",
                        help="Wolfram rule number (default: 30)")
    parser.add_argument("-w", "--width", type=int, default=79, metavar="CELLS",
                        help="cells per row (default: 79)")
    parser.add_argument("-n", "--generations", type=int, default=40, metavar="N",
                        help="rows to print (default: 40)")
    parser.add_argument("-s", "--seed", type=int, default=None,
                        help="seed the random first row")
    parser.add_argument("--single", action="store_true",
                        help="start from one cell in the middle")
    parser.add_argument("--ascii", action="store_true",
                        help="use # and . instead of blocks")
    parser.add_argument("--no-color", dest="color", action="store_false",
                        help="no ANSI colour")
    parser.add_argument("--show-rule", action="store_true",
                        help="print the rule table and exit")
    parser.add_argument("--version", action="version", version="ca1d " + __version__)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not 0 <= args.rule <= 255:
        parser.error("--rule must be between 0 and 255")
    if args.width < 1 or args.generations < 1:
        parser.error("--width and --generations must be at least 1")

    if args.show_rule:
        sys.stdout.write(_show_rule(args.rule) + "\n")
        return 0

    rows = run(
        args.rule,
        width=args.width,
        generations=args.generations,
        seed=args.seed,
        single=args.single,
    )
    on, off = ("#", ".") if args.ascii else (BLOCK, " ")
    lines = render(rows, on=on, off=off)
    colour = args.color and sys.stdout.isatty()

    for index, line in enumerate(lines):
        if not colour:
            sys.stdout.write(line.rstrip() + "\n")
        else:
            rgb = _row_colour(index, len(lines))
            sys.stdout.write(_paint(line.rstrip() or " ", rgb) + "\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
