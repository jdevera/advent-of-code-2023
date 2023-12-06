import argparse
import datetime
import logging
import os
from pathlib import Path

from aoc import days
from aoc.utils import Part, EnumNameAction


def parse_args(argv):
    """ Parse and validate command line arguments """
    parser = argparse.ArgumentParser(description="AoC launcher")

    parser.add_argument("--debug", "-D", action='store_true',
                        help="Enable additional debugging output")

    subparsers = parser.add_subparsers(help="Subcommands help", required=True, dest='command')

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--input", "-i",
                            nargs="?",
                            help="Input file, with the contents as obtained in the AoC",
                            default=None)

    run_parser.add_argument("--day", "-d", type=int,
                            help="The day of the puzzle you want to run. By default today's",
                            default=None,
                            )

    run_parser.add_argument("--part", "-p", type=Part, action=EnumNameAction,
                            default=Part.ALL,
                            help="Which part of the day puzzle to run")

    test_parser = subparsers.add_parser("test")
    test_parser.add_argument("--day", "-d", type=int,
                             help="The day of the puzzle you want to test. By default today's",
                             default=None,
                             )
    test_parser.add_argument("--all", action='store_true',
                             help="Run all tests.")

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

    if args.command == 'run':
        if args.input is None:
            args.input = Path(module.__file__).resolve().parent / "data" / "input"
        if not os.path.exists(args.input):
            parser.error(f"Could not find file {args.input}")

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        setattr(module, 'debug', True)

    return args
