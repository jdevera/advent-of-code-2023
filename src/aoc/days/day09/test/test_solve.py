import pytest

from aoc.days import day09 as today

# TODO: Write the solutions here once you have them verified
SOLUTIONS: tuple[str | None, ...] = (
    None,
    None
)

@pytest.mark.xfail  # TODO: Remove this once implemented
def test_first_example(input_file_factory):
    input_file = input_file_factory("""
        TODO: Replace with example for part 1, can be indented 
        """)
    assert today.solve_first(input_file) == 'SOLUTION TO PART 1'


@pytest.mark.xfail  # TODO: Remove this once implemented
def test_second_example(input_file_factory):
    input_file = input_file_factory("""
        TODO: Replace with example for part 2, can be indented 
        """)
    assert today.solve_second(input_file) == 'SOLUTION TO PART 2'


@pytest.mark.xfail  # TODO: Remove this once implemented
def test_first_solution(day_input):
    assert SOLUTIONS[0] is not None
    assert today.solve_first(day_input) == SOLUTIONS[0]


@pytest.mark.xfail  # TODO: Remove this once implemented
def test_second_solution(day_input):
    assert SOLUTIONS[1] is not None
    assert today.solve_second(day_input) == SOLUTIONS[1]
