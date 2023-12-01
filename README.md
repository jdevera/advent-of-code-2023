# Introduction
This is Jacobo de Vera's Advent Of Code 2023 Workbench.

# How does this work
There is a launcher `aoc.py` written in Python that assumes Python is used for the solution.

## Day folders
Each day is a Python module under `src/days` called `dayXX` where `XX` is the day number with leading zeroes.

The day to run can be chosen in the launcher with the `--day X` option (it does not need the leading zeroes.) By default
the launcher will run today's solvers (if it's December.)

## Puzzle Parts
Each day puzzle has two parts. The day module needs to expose two functions, one for each part, they are
called `solve_first` and `solve_second`.

These functions:
* Take a single parameter with the input file in a `pathlib.Path` object.
* Return either the solution as a string or `None`, if the solution is not yet implemented.

The launcher can choose which of those to run with the `--part {first,second,all}` parameter.

## Input data

The launcher expects your daily puzzle input to be in a file called `input` within the directory of the day. This is the
file it will pass to the solvers by default.

A different input file can be passed to the solvers by specifying it in the commend line as a positional parameter.

# Solving a puzzle

Let's assume Python is the language of choice. The day starts with a module that has stubs for the two solvers and 4 tests:
1. A test that runs your first solver with the first example input
1. A test that runs your second solver with the second example input
1. A test that runs your first solver with the full puzzle input
1. A test that runs your second solver with the full puzzle input

When starting with a solver, start with entering example data to the example test, so you can run it with every change
and check results.

Each day module has a logger configured at its top level, it's called `log`. When the launcher runs with the `--debug`
option, it's set to DEBUG level.

Use `log.debug` instead of `print`.

Return the solution as a string, the launcher will prerry print it for easy copying into the puzzle form.

# Solved Puzzles

When a puzzle is fully solved, the day module can have a file called `SOLVED` to signal this easily.

None of the tests should be marked as `xfail` when a puzzle is solved.

# Using other languages

The launcher will call a Python module with the described parameters and expect a string or None as the result. What happens inside is up to the person implementing that day's puzzle solution.

To make things easier, there is this:

`from aoc.utils import run_external_solver`

Which will run any programm you want and take the solution from `stdout`.








