import logging
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger(__name__)
_debug = False  # Whether we are in debug mode

LINE_PATTERN = re.compile(r"^Card\s+(\d+): (.+) \| (.+)$")


def _number_set(numbers: str):
    return set(int(num) for num in numbers.split())


@dataclass
class Card:
    id: int
    numbers: set[int]
    winning: set[int]
    matching: set[int]
    worth: int
    copies_won: list[int]

    @classmethod
    def from_line(cls, line: str):
        m = LINE_PATTERN.match(line)
        if not m:
            raise ValueError(f"Invalid line {line}")
        card_id = int(m.group(1))
        numbers = _number_set(m.group(2))
        winning = _number_set(m.group(3))
        matching = numbers.intersection(winning)
        worth = 2 ** (len(matching) - 1) if matching else 0
        copies_won = [card_id + next_card for next_card in range(1, len(matching) + 1)]

        return cls(
            id=card_id,
            numbers=numbers,
            winning=winning,
            matching=matching,
            worth=worth,
            copies_won=copies_won,
        )


def parse_input(input_file: Path):
    for line in input_file.read_text().splitlines():
        card = Card.from_line(line)
        log.debug(f"{card=}")
        yield card


def solve_first(input_file: Path) -> str | None:
    return str(sum(card.worth for card in parse_input(input_file)))


def solve_second(input_file: Path) -> str | None:
    cards = list(parse_input(input_file))
    card_counts = Counter()
    for card in cards:
        card_counts[card.id] += 1
        for _ in range(card_counts[card.id]):
            for copy_id in card.copies_won:
                card_counts[copy_id] += 1

    return str(sum(card_counts.values()))
