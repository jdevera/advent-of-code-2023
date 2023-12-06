import logging
import re
from typing import Generator, NamedTuple
from pathlib import Path

log = logging.getLogger(__name__)
_debug = False  ## Whether we are in debug mode

PATTERN = re.compile(r"(?P<number>\d+)|(?P<symbol>[^0-9.\n])")


class Number(NamedTuple):
    value: int
    line: int
    col_first: int
    col_last: int

    @classmethod
    def from_match(cls, match: re.Match, line_no: int):
        start, end = match.span()
        return cls(
            value=int(match.group("number")),
            line=line_no,
            col_first=start,
            col_last=end - 1,
        )

    def is_adjacent_to(self, symbol: "Symbol"):
        if abs(symbol.line - self.line) > 1:
            return False
        return self.col_first - 1 <= symbol.col <= self.col_last + 1


class Symbol(NamedTuple):
    value: str
    line: int
    col: int

    @classmethod
    def from_match(cls, match: re.Match, line_no: int):
        value = match.group("symbol")
        start, end = match.span()
        if end - start != 1:
            raise ValueError(f"Invalid Symbol {value}. Too long!")
        return cls(value=value, line=line_no, col=start)

    def gear_ratio(self, numbers: set[Number]) -> int | None:
        """
        Provide gear ratio, or None if this is not a gear
        """
        if self.value != "*":
            return None
        adjacent_numbers = []
        for number in numbers:
            if number.is_adjacent_to(self):
                if len(adjacent_numbers) >= 2:
                    return None
                adjacent_numbers.append(number)
        if len(adjacent_numbers) != 2:
            return None
        num1, num2 = adjacent_numbers
        return num1.value * num2.value


def parse_input(input_content: str) -> tuple[set[Symbol], set[Number]]:
    symbols: set[Symbol] = set()
    numbers: set[Number] = set()
    for line_no, line in enumerate(input_content.splitlines()):
        for m in PATTERN.finditer(line):
            if m.group("symbol") is not None:
                symbol = Symbol.from_match(m, line_no)
                symbols.add(symbol)
                log.debug("Symbol %s at %s", symbol.value, (symbol.line, symbol.col))
            elif m.group("number") is not None:
                number = Number.from_match(m, line_no)
                numbers.add(number)
                log.debug(
                    "Number %s at %s", number.value, (number.line, number.col_first)
                )
    return symbols, numbers


def get_parts(symbols: set[Symbol], numbers: set[Number]) -> Generator[int, None, None]:
    for number in numbers:
        if any(number.is_adjacent_to(symbol) for symbol in symbols):
            yield number.value


def get_gear_ratios(
    symbols: set[Symbol], numbers: set[Number]
) -> Generator[int, None, None]:
    for symbol in symbols:
        ratio = symbol.gear_ratio(numbers)
        if ratio is not None:
            yield ratio


def solve_first(input_file: Path) -> str:
    symbols, numbers = parse_input(input_file.read_text())
    return str(sum(get_parts(symbols, numbers)))


def solve_second(input_file: Path) -> str:
    symbols, numbers = parse_input(input_file.read_text())
    return str(sum(get_gear_ratios(symbols, numbers)))
