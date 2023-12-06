import re
import logging
from pathlib import Path

log = logging.getLogger(__name__)
_debug = False  ## Whether we are in debug mode

NUMBERS = {
    'one': '1', 'two': '2', 'three': '3',
    'four': '4', 'five': '5', 'six': '6',
    'seven': '7', 'eight': '8', 'nine': '9',
}


def solve_first(input_file: Path):
    with input_file.open("r") as fin:
        total = 0
        for line in fin:
            digits = [c for c in line if str.isnumeric(c)]
            calibration = int(digits[0] + digits[-1])
            total += calibration

            log.debug(f"{digits=}")
            log.debug(f"{calibration=}")
            log.debug(f"{total=}")
    return str(total)


def _get_digits_with_names(line: str) -> list[str]:
    # Make a pattern oring all digits and number names
    pattern = f"{'|'.join(list(NUMBERS.keys()) + list(NUMBERS.values()))}"
    regex = re.compile(pattern)

    values = []

    # User re.search with a position parameter to ensure we consider digit names
    # that are overlapping (by starting the next search one character after the
    # start of the last match.)
    pos = 0
    while m := regex.search(line, pos):
        pos = m.start() + 1
        values.append(m.group(0))

    log.debug(f"{values=}")

    def _to_digit(value):
        """Turn '1' or 'one' into '1', '2' or 'two' into '2', etc."""
        return value if value.isnumeric() else str(NUMBERS.get(value))

    return [_to_digit(v) for v in (values[0], values[-1])]


def solve_second(input_file: Path):
    with input_file.open("r") as fin:
        total = 0
        for lineno, line in enumerate(fin):
            log.debug(f"\n{lineno + 1} -> {line.strip()}")

            digits = _get_digits_with_names(line)
            calibration = int(digits[0] + digits[-1])
            total += calibration

            log.debug(f"{digits=}")
            log.debug(f"{calibration=}")
            log.debug(f"{total=}")
    return str(total)
