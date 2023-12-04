import argparse
import logging
import sys
from pathlib import Path

from aoc.launcher.args import parse_args
from aoc.utils import Part


def print_solution(day: int, part: Part, solution: str | None):
    title = f"Solution to Day {day}, {part.name.capitalize()} Part"
    if solution is None:
        print(f"No {title} ❌")
    else:
        print(title)
        print("-" * len(title))
        print(solution)
        print("-" * len(title))
    print()


def command_run(args: argparse.Namespace):
    if args.part.includes(Part.FIRST):
        first = args.module.solve_first(args.input)
        print_solution(args.day, Part.FIRST, solution=first)
    if args.part.includes(Part.SECOND):
        second = args.module.solve_second(args.input)
        print_solution(args.day, Part.SECOND, solution=second)


def command_test(args: argparse.Namespace):
    import pytest
    pytest_args = []
    if not args.all:
        pytest_args.append(Path(args.module.__file__).parent)
    if args.debug:
        pytest_args.append('--log-cli-level=DEBUG')
    logging.debug("running pytest with %s", pytest_args)
    pytest.main(pytest_args)


def main(argv=None):
    """ Run this program """
    if argv is None:
        argv = [__name__]
    args = parse_args(argv)
    try:
        if args.command == 'run':
            command_run(args)
        elif args.command == 'test':
            command_test(args)
        else:
            raise NotImplementedError(f"Command not implemented: {args.command}")
    except KeyboardInterrupt:
        sys.exit(-1)
