import enum
import logging
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

log = logging.getLogger(__name__)
_debug = False  # Whether we are in debug mode

CARD_VALUES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
}

JOKER = "J"
JOKER_VALUE = 1
CARDS_IN_HAND = 5


def _get_card_value(card_name: str, with_jokers: bool):
    if with_jokers and card_name == JOKER:
        return JOKER_VALUE
    value = CARD_VALUES.get(card_name)
    return value if value is not None else int(card_name)


@dataclass(frozen=True, order=True)
class HandTypeValue:
    spec: tuple[int, ...] = field(compare=False)
    value: int


class HandType(enum.Enum):
    FIVE_OF_A_KIND = HandTypeValue(spec=(5,), value=7)
    FOUR_OF_A_KIND = HandTypeValue(spec=(4, 1), value=6)
    FULL_HOUSE = HandTypeValue(spec=(3, 2), value=5)
    THREE_OF_A_KIND = HandTypeValue(spec=(3, 1, 1), value=4)
    TWO_PAIR = HandTypeValue(spec=(2, 2, 1), value=3)
    ONE_PAIR = HandTypeValue(spec=(2, 1, 1, 1), value=2)
    HIGH_CARD = HandTypeValue(spec=(1, 1, 1, 1, 1), value=1)

    @classmethod
    def from_hand(cls, hand: 'Hand'):
        count = Counter(hand.effective_hand)
        sorted_counts: list[tuple[str, int]] = count.most_common()
        spec = tuple(num for _, num in sorted_counts)
        for element in cls:
            if element.value.spec == spec:
                return element
        return None


@dataclass(frozen=True)
class Hand:
    cards: str
    bid: int
    with_jokers: bool
    type: HandType = field(init=False)
    _card_values: tuple[int] = field(init=False)

    def __post_init__(self):

        if len(self.cards) != CARDS_IN_HAND:
            raise ValueError(f"Hands must have exactly {CARDS_IN_HAND} cards, found {len(self.cards)}")

        card_values = tuple(_get_card_value(card, self.with_jokers) for card in self.cards)
        object.__setattr__(self, 'type', HandType.from_hand(self))
        object.__setattr__(self, '_card_values', card_values)

    @property
    def effective_hand(self) -> str:
        if not self.with_jokers or JOKER not in self.cards or self.cards == JOKER * CARDS_IN_HAND:
            return self.cards
        count = Counter(card for card in self.cards if card != JOKER)
        max_card = count.most_common()[0][0]
        return self.cards.replace(JOKER, max_card)

    @classmethod
    def from_line(cls, line: str, with_jokers: bool) -> 'Hand':
        cards, bid = line.split()
        return cls(cards=cards, bid=int(bid), with_jokers=with_jokers)

    def __lt__(self, other: 'Hand') -> bool:
        if self.type != other.type:
            return self.type.value.value < other.type.value.value
        return self._card_values < other._card_values


def get_total(input_file: Path, *, with_jokers: bool) -> str:
    hands = sorted([Hand.from_line(line, with_jokers) for line in input_file.read_text().splitlines()])
    total = 0
    for rank, hand in enumerate(hands, start=1):
        log.debug("Hand: %s (%s) → type: %s, rank: %d", hand.cards, hand.effective_hand, hand.type.name, rank)
        total += (rank * hand.bid)
    return str(total)


def solve_first(input_file: Path) -> str | None:
    return get_total(input_file, with_jokers=False)


def solve_second(input_file: Path) -> str | None:
    return get_total(input_file, with_jokers=True)
