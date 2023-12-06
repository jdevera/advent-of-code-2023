import re
from dataclasses import dataclass, astuple
import logging
from pathlib import Path

log = logging.getLogger(__name__)
_debug = False  ## Whether we are in debug mode

CUBE_LIMITS = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


@dataclass
class CubeSet:
    red: int
    green: int
    blue: int

    def __post_init__(self):
        rgb_values = (self.red, self.green, self.blue)
        if rgb_values == (0, 0, 0):
            raise ValueError("Zero Set not valid")
        if any(v < 0 for v in rgb_values):
            raise ValueError("Negative values not allowed")

    def possible_with(self, available_cubes: 'CubeSet'):
        return all(e1 <= e2 for (e1, e2) in zip(astuple(self), astuple(available_cubes)))

    @classmethod
    def from_line(cls, play: str):
        colour_pattern = re.compile(r'(\d+) (red|green|blue)')
        cubes = {colour: 0 for colour in ('red', 'green', 'blue')}
        play_cubes = {colour: int(number) for number, colour in colour_pattern.findall(play)}

        result = cls(**dict(cubes, **play_cubes))
        log.debug("Extracted %s -> %s", play_cubes, result)
        return result


@dataclass
class Game:
    id: int
    plays: list[CubeSet]

    @classmethod
    def from_line(cls, line: str):
        game_pattern = re.compile(r'Game (\d+): (.+)\s*')
        m = game_pattern.match(line)
        if not m:
            raise ValueError(f"Unexpected line format: {line}")
        game_id, plays_spec = m.groups()
        plays = plays_spec.split("; ")
        return cls(id=int(game_id), plays=[CubeSet.from_line(play) for play in plays])

    def possible_with(self, available_cubes: CubeSet):
        return all(play.possible_with(available_cubes) for play in self.plays)

    @property
    def power(self):
        plays_by_colour = zip(*(astuple(play) for play in self.plays))
        red, green, blue = [max(col) for col in plays_by_colour]
        return red * green * blue


def solve_first(input_file: Path) -> str | None:
    with input_file.open("r") as fin:
        max_cubes = CubeSet(**CUBE_LIMITS)
        games = (Game.from_line(line) for line in fin)
        possible_games = (game for game in games if game.possible_with(max_cubes))
        total = sum(game.id for game in possible_games)
        return str(total)


def solve_second(input_file: Path) -> str | None:
    with input_file.open("r") as fin:
        return str(sum(Game.from_line(line).power for line in fin))
