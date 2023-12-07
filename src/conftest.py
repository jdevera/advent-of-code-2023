import logging
from pathlib import Path
from textwrap import dedent
import pytest

FILE_NAME_INPUT = 'input'
FILE_NAME_SOLUTION_PART_1 = 'part1.solution'
FILE_NAME_SOLUTION_PART_2 = 'part2.solution'


@pytest.fixture
def input_file_factory(tmp_path):
    """
    Creates a temporary input file with the given contents
    """

    def mkinput(content):
        assert content[0] == '\n'
        content = dedent(content)[1:]
        file = tmp_path / FILE_NAME_INPUT
        file.write_text(content)
        return file

    yield mkinput


@pytest.fixture
def day_data_dir(request: pytest.FixtureRequest) -> Path:
    return request.path.resolve().parent.parent / 'data'


@pytest.fixture
def tested_day(request: pytest.FixtureRequest) -> int:
    day_module_name = request.path.resolve().parent.parent.name
    assert day_module_name.startswith("day")
    return int(day_module_name[3:])


@pytest.fixture
def day_input(day_data_dir: Path, tested_day: int) -> Path:
    """
    Get the file called input that lives in the day module.
    This assumes tests are under a "test" module in the day folder
    """
    input_file = day_data_dir / FILE_NAME_INPUT
    if not input_file.exists():
        from aocd.get import current_day
        from aoc.utils import fetch_input
        if tested_day > current_day():
            logging.info("Input file for day %d not yet available", tested_day)
            return None
        logging.info("Could not find %s, will download", str(input_file))
        fetch_input(tested_day)

    assert input_file.exists()
    yield input_file


def _get_solution(solution_file: Path):
    if not solution_file.exists():
        return None
    lines = solution_file.read_text().splitlines()
    if not lines:
        return None
    return lines[0]


@pytest.fixture
def part1_solution(day_data_dir: Path) -> str | None:
    return _get_solution(day_data_dir / FILE_NAME_SOLUTION_PART_1)


@pytest.fixture
def part2_solution(day_data_dir: Path) -> str | None:
    return _get_solution(day_data_dir / FILE_NAME_SOLUTION_PART_2)
