import pytest

from aoc.days.day02 import CubeSet

LIMIT = CubeSet(12, 13, 14)


@pytest.mark.parametrize('rgb,possible', (
        ((2, 5, 18), False),
        ((12, 11, 15), False),
        ((20, 10, 2), False),
        ((1, 1, 1), True),
        ((12, 13, 14), True),
))
def test_possible(rgb, possible):
    assert CubeSet(*rgb).possible_with(LIMIT) == possible
