from aoc.days import day07 as today

EXAMPLE_INPUT = """
    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483
"""


def test_first_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_first(input_file) == '6440'


def test_second_example(input_file_factory):
    input_file = input_file_factory(EXAMPLE_INPUT)
    assert today.solve_second(input_file) == '5905'


def test_first_solution(day_input, part1_solution):
    assert today.solve_first(day_input) == part1_solution
    assert part1_solution is not None


def test_second_solution(day_input, part2_solution):
    assert part2_solution is not None
    assert today.solve_second(day_input) == part2_solution


def test_lt_hand():
    ktjjt = today.Hand("KTJJT", bid=1, with_jokers=True)
    qqqja = today.Hand("QQQJA", bid=1, with_jokers=True)
    assert qqqja < ktjjt