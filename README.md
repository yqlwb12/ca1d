# ca1d

**Wolfram's elementary cellular automata, one row at a time.** Rule numbers 0–255, a terminal, no dependencies.

```console
$ ca1d -r 30 --single -w 61 -n 16 --ascii
..............................#..............................
.............................###.............................
............................##..#............................
...........................##.####...........................
..........................##..#...#..........................
.........................##.####.###.........................
........................##..#....#..#........................
.......................##.####..######.......................
......................##..#...###.....#......................
.....................##.####.##..#...###.....................
....................##..#....#.####.##..#....................
...................##.####..##.#....#.####...................
..................##..#...###..##..##.#...#..................
.................##.####.##..###.###..##.###.................
................##..#....#.###...#..###..#..#................
...............##.####..##.#..#.#####..#######...............
```

Sixteen rows is enough to recognise it: that is rule 30, the one Stephen Wolfram used
to argue that simple rules produce irreducible complexity. The same three lines of
code produce Sierpinski gaskets (rule 90), class-4 chaos (rule 110 — proven
Turing-complete), and the trivial ones (0, 51, 204, 255).

## Why

Because it is the smallest interesting program I know of: one byte of rule, one row
of cells, and out comes a shape nobody predicted. It also makes a good test case —
every claim about the code can be checked against a known picture.

## Install

```console
$ pip install .
$ ca1d                     # rule 30, 79 wide, 40 rows, random seed
```

Or straight from the checkout: `PYTHONPATH=src python -m ca1d`.

## Usage

```console
$ ca1d -r 110 -n 60 -w 120     # the Turing-complete one
$ ca1d -r 90 --single          # Sierpinski gasket
$ ca1d -r 45 -s 7              # reproducible random start
$ ca1d --show-rule 30          # print the Wolfram table
$ ca1d --ascii                 # # and . instead of full blocks
$ ca1d --no-color > rules.txt  # plain text for a file
```

| Option | Meaning |
| --- | --- |
| `-r, --rule` | rule number, 0–255 (default 30) |
| `-w, --width` | cells per row (default 79) |
| `-n, --generations` | rows to print (default 40) |
| `-s, --seed` | seed the random first row |
| `--single` | start from one cell in the middle |
| `--ascii` | `#` and `.` instead of `█` |
| `--no-color` | never emit ANSI |
| `--show-rule` | print the rule's lookup table |

With a terminal that speaks 24-bit colour the rows shade from blue to amber, which
makes the direction of time obvious at a glance.

## The rule table

```console
$ ca1d --show-rule 30
111 110 101 100 011 010 001 000
  0   0   0   1   1   1   1   0
```

Read a neighbourhood as a binary number — `111` is 7, `000` is 0 — and the rule
number's bits say what the centre cell becomes next generation. Rule 30 is
`00011110` in binary, which is where the number comes from.

## How it works

1. `decode_rule` turns one integer into an eight-entry table: `table[n] = (rule >> n) & 1`.
2. `step` walks the row, reads `4·left + 2·centre + right`, and looks it up. The row
   is a torus: the neighbour of the first cell is the last cell.
3. `run` repeats that, keeping every generation so you can draw the history.

## Tests

```console
$ PYTHONPATH=src python -m unittest discover -s tests -v
```

28 tests, no test dependencies. They pin the rule tables (30, 51, 204), the
Sierpinski gasket that rule 90 must produce, torus wrapping, determinism under a
seed, and the CLI's argument handling.

## Licence

MIT.
