import logging
from aoc.days import day02 as today

logging.basicConfig(level=logging.DEBUG)

EXAMPLE_INPUT = """
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """


def test_first_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_first(input_file) == '8'


def test_second_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_second(input_file) == '2286'


def test_first_solution(day_input, part1_solution):
    assert part1_solution is not None
    assert today.solve_first(day_input) == part1_solution


def test_second_solution(day_input, part2_solution):
    assert part2_solution is not None
    assert today.solve_second(day_input) == part2_solution
