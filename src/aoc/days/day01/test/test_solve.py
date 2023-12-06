from aoc.days import day01 as today


def test_first_example(input_file_factory):
    input_file = input_file_factory("""
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet
        """)
    assert today.solve_first(input_file) == '142'


def test_second_example(input_file_factory):
    input_file = input_file_factory("""
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen
        """)
    assert today.solve_second(input_file) == '281'


def test_first_solution(day_input, part1_solution):
    assert part1_solution is not None
    assert today.solve_first(day_input) == part1_solution


def test_second_solution(day_input, part2_solution):
    assert part2_solution is not None
    assert today.solve_second(day_input) == part2_solution
