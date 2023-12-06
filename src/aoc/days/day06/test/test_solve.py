from aoc.days import day06 as today

EXAMPLE_INPUT = """
    Time:      7  15   30
    Distance:  9  40  200
    """


def test_first_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_first(input_file) == '288'


def test_second_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_second(input_file) == '71503'


def test_first_solution(day_input, part1_solution):
    assert today.solve_first(day_input) == part1_solution
    assert part1_solution is not None


def test_second_solution(day_input, part2_solution):
    assert today.solve_second(day_input) == part2_solution
    assert part2_solution is not None
