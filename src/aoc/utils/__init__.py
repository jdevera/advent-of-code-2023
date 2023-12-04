import os
import subprocess
from enum import Enum, auto

import argparse
import enum
from pathlib import Path


class EnumNameAction(argparse.Action):
    """
    Argparse action for handling Enums
    https://stackoverflow.com/a/60750535
    """

    def __init__(self, **kwargs):
        # Pop off the type value
        enum_type = kwargs.pop("type", None)

        # Ensure an Enum subclass is provided
        if enum_type is None:
            raise ValueError(
                "type must be assigned an Enum when using EnumAction")
        if not issubclass(enum_type, enum.Enum):
            raise TypeError("type must be an Enum when using EnumAction")

        # Generate choices from the Enum
        value_map = {e.name.lower(): e for e in enum_type}
        kwargs.setdefault("choices", tuple(value_map.keys()))

        super().__init__(**kwargs)

        self._enum = enum_type
        self._value_map = value_map

    def __call__(self, parser, namespace, values, option_string=None):
        # Convert value back into an Enum

        value = self._value_map[values]
        setattr(namespace, self.dest, value)


class Part(Enum):
    FIRST = auto()
    SECOND = auto()
    ALL = auto()

    def includes(self, part: 'Part'):
        return self in (part, Part.ALL)


def run_external_solver(command: list[str], *, debug: bool = False,
                        input_path: Path | None = None):
    """
    Run an external solver.
    You can choose to pass anything as command line parameters, and these can
    be optionally included in the environment
    * If we are in debug mode, pass the var AOC_DEBUG set to 1
    * If the input path is given, pass it in the AOC_INPUT_PATH var
    """
    env = os.environ.copy()
    if debug:
        env['AOC_DEBUG'] = '1'
    if input_path is not None:
        env['AOC_INPUT_PATH'] = str(input_path)

    solver = subprocess.Popen(command, stdout=subprocess.PIPE, env=env, encoding='utf-8')
    stdout, _ = solver.communicate()
    solver.wait()
    if solver.returncode != 0:
        raise Exception(f"Command exited with rc={solver.returncode}")
    return stdout


def emojify_flag(flag: bool | None):
    if flag is None:
        return "⬜️"
    return "✅" if flag else "❌"
