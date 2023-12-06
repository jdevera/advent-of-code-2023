
from aoc.days import day05 as today

EXAMPLE_INPUT = """
        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4
"""


def test_first_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_first(input_file) == "35"


def test_second_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_second(input_file) == "46"


def test_first_solution(day_input, part1_solution):
    assert part1_solution is not None
    assert today.solve_first(day_input) == part1_solution


def test_second_solution(day_input, part2_solution):
    assert part2_solution is not None
    assert today.solve_second(day_input) == part2_solution
