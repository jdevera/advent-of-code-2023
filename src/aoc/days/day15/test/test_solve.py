import pytest

from aoc.days import day15 as today

EXAMPLE_INPUT = """
        TODO: Replace with example input, can be indented 
"""


# TODO: Write the solutions in the part1.solution and part2.solution files once you have them verified

@pytest.mark.xfail  # TODO: Remove this once implemented
def test_first_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_first(input_file) == 'SOLUTION TO PART 1'


@pytest.mark.xfail  # TODO: Remove this once implemented
def test_second_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_second(input_file) == 'SOLUTION TO PART 2'


@pytest.mark.xfail  # TODO: Remove this once implemented
def test_first_solution(day_input, part1_solution):
    assert today.solve_first(day_input) == part1_solution
    assert part1_solution is not None


@pytest.mark.xfail  # TODO: Remove this once implemented
def test_second_solution(day_input, part2_solution):
    assert part2_solution is not None
    assert today.solve_second(day_input) == part2_solution
