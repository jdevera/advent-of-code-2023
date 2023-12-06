import logging
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

from cmath import sqrt
from math import ceil, floor

log = logging.getLogger(__name__)
_debug = False  # Whether we are in debug mode


@dataclass
class Race:
    time: int
    distance: int


class InputFormat(Enum):
    MULTI_RACE = auto()
    SINGLE_RACE = auto()


def parse_line(line: str, input_format: InputFormat):
    label, *values = line.split()
    if input_format == InputFormat.MULTI_RACE:
        return [int(val) for val in values]
    else:
        return [int("".join(values))]


def parse_input(input_file: Path, input_format: InputFormat):
    time_line, distance_line = input_file.read_text().splitlines()
    assert time_line.startswith("Time:")
    assert distance_line.startswith("Distance:")
    times = parse_line(time_line, input_format)
    distances = parse_line(distance_line, input_format)

    assert len(times) == len(distances)
    return [Race(time, distance) for time, distance in zip(times, distances)]


def solve_for_x(a, b, c):
    return [(-b + factor * sqrt(b ** 2 - 4 * a * c)) / -2 for factor in [1, -1]]


def ways_to_win_power(input_file: Path, input_format: InputFormat) -> str | None:
    races = parse_input(input_file, input_format)
    log.debug(f"{races=}")
    total = 1
    for race in races:
        log.debug("Checking race: %s", race)
        edges = solve_for_x(a=-1, b=race.time, c=-race.distance)

        log.debug("edges %s", edges)
        start_winning = floor(edges[0].real) + 1
        start_losing = ceil(edges[1].real)

        total *= (start_losing - start_winning)

    return str(total)


def solve_first(input_file: Path) -> str | None:
    return ways_to_win_power(input_file, InputFormat.MULTI_RACE)


def solve_second(input_file: Path) -> str | None:
    return ways_to_win_power(input_file, InputFormat.SINGLE_RACE)
