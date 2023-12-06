# Introduction
This is Jacobo de Vera's Advent Of Code 2023 Workbench.

> [!WARNING]
> ⚠️ **SPOILER ALERT**: This repository contains my solutions (but not my input) ⚠️

# How does this work
There is a launcher written in Python that assumes Python is used for
the solution.

```shell
cd src
python -m aoc --help
```

## Day folders
Each day is a Python module under `src/aoc/days` called `dayXX` where `XX` is the
day number with leading zeroes.

The day to run can be chosen in the launcher with the `--day X` option (it does
not need the leading zeroes.) By default, the launcher will run today's solvers
(if it's December.)

## Puzzle Parts

Each day puzzle has two parts. The day module needs to expose two functions,
one for each part, they are called `solve_first` and `solve_second`.

These functions:
* Take a single parameter with the input file in a `pathlib.Path` object.
* Return either the solution as a string or `None`, if the solution is not yet
  implemented.

The launcher can choose which of those to run with the 
`--part {first,second,all}` parameter.

## Input data

The launcher expects your daily puzzle input to be in a file called `input` under `src/aoc/days/dayXX/data` within the
directory of the day. This is the file it will pass to the solvers by default.

A different input file can be passed to the solvers by specifying it in the command line with the `--input` flag.

# Solving a puzzle

Let's assume Python is the language of choice. The day starts with a module
that has stubs for the two solvers under `src/aoc/days/dayXX/__init__.py`.

## Tests

Each day starts with four tests under the `test` directory of the day, which
are marked as expected to fail:

1. A test that runs your first solver with the first example input
1. A test that runs your second solver with the second example input
1. A test that runs your first solver with the full puzzle input
1. A test that runs your second solver with the full puzzle input

When starting with a solver, start with entering example data to the example
test, so you can run it with every change and check results.

You can run tests with pytest or with `python -m aoc test`, which will run
pytest for you.

Don't forget to clear the `xfail` marker once you have started working on a
day's puzzle.

## ~~Printing~~ Logging
Each day module has a logger configured at its top level, it's called `log`.
When the launcher runs with the `--debug` option, it's set to DEBUG level.

Use `log.debug` instead of `print`.

## Solution
Return the solution *as a string*, the launcher will pretty print it for easy
copying into the puzzle form on the AoC website.

# Using other languages

The launcher will call a Python module with the described parameters and expect
a string or None as the result. What happens inside is up to the person
implementing that day's puzzle solution.

To make things easier, there is this:

`from aoc.utils import run_external_solver`

Which will run any program you want and take the solution from `stdout`.


