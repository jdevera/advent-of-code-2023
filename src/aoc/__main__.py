#!/usr/bin/env python
# -*- coding: utf-8 -*-

__description__ = ''

import datetime
import logging
import os.path
import sys
import argparse
from pathlib import Path
from aoc import days
from aoc.utils import Part, EnumNameAction


def parse_args(argv):
    """ Parse and validate command line arguments """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input",
                        nargs="?",
                        help="Input file, with the contents as obtained in the AoC",
                        default=None)

    parser.add_argument("--day", type=int,
                        help="The day of the puzzle you want to run. By default today's",
                        default=None,
                        )

    parser.add_argument("--part", "-p", type=Part, action=EnumNameAction,
                        default=Part.ALL,
                        help="Which part of the day puzzle to run")

    parser.add_argument("-d", "--debug", action='store_true',
                        help="Enable additional debugging output")

    args = parser.parse_args(argv[1:])

    if args.day is None:
        today = datetime.date.today()
        if today.month != 12:
            parser.error("Not in December, cannot infer day, use --day N")
        args.day = today.day

    module = getattr(days, f"day{args.day:02d}", None)

    if module is None:
        parser.error(
            f"Could not find code for that day: {args.day}. Try between 1 and 25.")

    setattr(args, "module", module)

    if args.input is None:
        args.input = Path(module.__file__).resolve().parent / "input"
    if not os.path.exists(args.input):
        parser.error(f"Could not find file {args.input}")

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        setattr(module, 'debug', True)
        os.environ['AOC_DEBUG'] = '1'

    return args


def print_solution(part: Part, solution: str | None):
    title = f"Solution to {part.name.capitalize()} Part"
    if solution is None:
        print(f"No {title} ❌")
    else:
        print(title)
        print("-" * len(title))
        print(solution)
        print("-" * len(title))
    print()


def main(argv=None):
    """ Run this program """
    if argv is None:
        argv = [__name__]
    args = parse_args(argv)
    try:
        if args.part.includes(Part.FIRST):
            first = args.module.solve_first(args.input)
            print_solution(Part.FIRST, solution=first)
        if args.part.includes(Part.SECOND):
            second = args.module.solve_second(args.input)
            print_solution(Part.SECOND, solution=second)

    except KeyboardInterrupt:
        sys.exit(-1)


if __name__ == '__main__':
    sys.exit(main(sys.argv) or 0)
