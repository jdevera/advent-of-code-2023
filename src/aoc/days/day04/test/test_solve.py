from aoc.days import day04 as today

EXAMPLE_INPUT = """
        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def test_first_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_first(input_file) == '13'


def test_second_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_second(input_file) == '30'


def test_first_solution(day_input, part1_solution):
    assert part1_solution is not None
    assert today.solve_first(day_input) == part1_solution


def test_second_solution(day_input, part2_solution):
    assert part2_solution is not None
    assert today.solve_second(day_input) == part2_solution