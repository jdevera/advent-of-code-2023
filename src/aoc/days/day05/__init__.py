import itertools
import logging
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

log = logging.getLogger(__name__)
_debug = False  # Whether we are in debug mode

MAP_ORDER = ['seed-to-soil',
             'soil-to-fertilizer',
             'fertilizer-to-water',
             'water-to-light',
             'light-to-temperature',
             'temperature-to-humidity',
             'humidity-to-location']


@dataclass(frozen=True)
class Range:
    first: int
    length: int = 1

    @property
    def last(self):
        return self.first + self.length - 1

    def __contains__(self, item: int):
        return self.first <= item <= self.last

    def __len__(self):
        return self.length

    def __str__(self):
        return f"{self.__class__.__name__}[first:{self.first:,}, last:{self.last:,}, len:{self.length:,}]"

    def __lt__(self, other):
        return self.first < other.first

    def split_at(self, value) -> list['Range']:
        if value not in self or value == self.first:
            return [self]
        range1 = Range(self.first, value - self.first)
        range2 = Range(value, self.length - range1.length)
        return [
            range1, range2
        ]


def _get_gaps(ranges: list['Range']) -> list['Range'] | None:
    if len(ranges) < 2:
        return None
    gaps = []
    last = ranges[0]
    for rng in ranges[1:]:
        gap_size = rng.first - last.last - 1
        if gap_size:
            gap = Range(last.last + 1, gap_size)
            gaps.append(gap)
        last = rng
    return gaps


@dataclass
class MultiRange:
    """
    An iterable made out of a collection of non-contiguous int ranges
    """
    ranges: list[Range] = field(default_factory=list)

    def __post_init__(self):
        self.ranges.sort()

    def add_range(self, first, length):
        self.ranges.append(Range(first, length))
        self.ranges.sort()

    def __iter__(self):
        return iter(itertools.chain(*self.ranges))

    def __len__(self):
        return sum(len(rng) for rng in self.ranges)

    @property
    def gaps(self):
        return _get_gaps(self.ranges)

    @property
    def full_range(self) -> Range | None:
        if not self.ranges:
            return None
        first = self.ranges[0].first
        last = self.ranges[-1].last
        full_range = Range(first, last - first + 1)
        return full_range


@dataclass(frozen=True)
class RangeMap:
    """
    Maps values from one source range to a destination range
    """
    source: Range
    offset: int

    @classmethod
    def from_line(cls, line: str) -> 'RangeMap':
        dest, orig, length = (int(part) for part in line.split())
        return cls(Range(orig, length), dest - orig)

    def __str__(self):
        return f"{self.__class__.__name__}[s:{self.source}  --> o:{self.offset}]"

    def __lt__(self, other):
        return self.source.first < other.source.first


@dataclass(frozen=True)
class MultiRangeMap:
    name: str
    range_maps: list[RangeMap]
    full_range: Range = field(init=False, repr=False, hash=False)

    def __post_init__(self):
        range_maps = list(sorted(self.range_maps))
        first = range_maps[0].source.first
        last = range_maps[-1].source.last
        full_range = Range(first, last - first + 1)
        object.__setattr__(self, 'range_maps', range_maps)
        object.__setattr__(self, 'full_range', full_range)

    def get_map_for(self, value: int) -> RangeMap:
        if not self.range_maps:
            return RangeMap(Range(0, sys.maxsize), 0)

        if value < self.full_range.first:
            return RangeMap(Range(0, self.full_range.first), 0)
        if value > self.full_range.last:
            return RangeMap(Range(self.full_range.last + 1, sys.maxsize - self.full_range.last), 0)
        for a_map in self.range_maps:
            if value < a_map.source.first:
                break
            if value in a_map.source:
                return a_map
        for gap in self.gaps:
            if value in gap:
                return RangeMap(gap, 0)

        raise NotImplementedError(f"Wrong assumption, should ahve found a map for: {value}")

    def apply(self, input_ranges: MultiRange):
        transitioned_ranges = MultiRange()

        # Put the input ranges in a stack. Check if a mapping can be applied to each range in full and if this is
        # not possible, split the range into a new range that can be mapped, and another that cannot. Then push this
        # latter one to the top of the stack to repeat the process.
        # In the end there should be a collection of input ranges that represent the same elements as the original set
        # but where each of them could be mapped with a single mapping.
        # The mapping, in this case, is simply to add an offset to the first element.
        input_range_stack = input_ranges.ranges[:]

        while input_range_stack:
            if _debug:
                for r in input_range_stack:
                    log.debug("Stack: %s", r)

            seed_range = input_range_stack.pop(0)
            a_map = self.get_map_for(seed_range.first)
            if seed_range.last <= a_map.source.last:
                # Full range of seeds included in this mapping
                log.debug("Seeds %s fit in mapping %s", seed_range, a_map)
                transitioned_ranges.add_range(seed_range.first + a_map.offset, seed_range.length)
            else:
                # Break this down into one that fits and put the rest back in the stac
                range_that_fits, excess = seed_range.split_at(a_map.source.last + 1)
                transitioned_ranges.add_range(range_that_fits.first + a_map.offset, range_that_fits.length)

                # And the rest goes back in the stack
                input_range_stack.insert(0, excess)

                log.debug("Seeds %s do not fit in mapping %s", seed_range, a_map)
                log.debug("Split into range that fits: %s", range_that_fits)
                log.debug("And a range that does not, which goes back to the stack: %s", excess)

        log.debug("Next ranges: %s", transitioned_ranges)
        return transitioned_ranges

    @property
    def gaps(self):
        if len(self.range_maps) < 2:
            return None
        gaps = _get_gaps([rm.source for rm in self.range_maps])
        return gaps


class SeedFormat(Enum):
    PLAIN = auto()
    RANGES = auto()


def parse_seed_ranges(seeds: list[int], seed_format: SeedFormat) -> MultiRange:
    ranges = MultiRange()
    if seed_format == SeedFormat.RANGES:
        assert len(seeds) % 2 == 0
        while seeds:
            first, length = seeds[:2]
            ranges.add_range(first, length)
            seeds = seeds[2:]
    else:
        for first in seeds:
            ranges.add_range(first, 1)

    return ranges


def parse_input(input_file: Path, seed_format: SeedFormat) -> tuple[MultiRange, list[MultiRangeMap]]:
    current_map = None
    seeds = None
    maps = defaultdict(list)
    for line in input_file.read_text().splitlines():
        if line.startswith("seeds: "):
            assert seeds is None
            seed_values = [int(seed) for seed in line.split(': ')[1].split()]
            seeds = parse_seed_ranges(seed_values, seed_format)
            log.debug(f"{seeds=}")
        elif line.endswith(" map:"):
            current_map = line.split()[0]
        elif not line:
            if current_map is not None:
                log.debug("map finished %s: %s", current_map, maps[current_map])
                current_map = None
        else:
            if current_map is None:
                raise ValueError(f"bad line {line}")
            maps[current_map].append(RangeMap.from_line(line))
    maps_by_name = {name: MultiRangeMap(name, range_maps) for name, range_maps in maps.items()}
    maps_in_order = [maps_by_name[name] for name in MAP_ORDER]
    return seeds, maps_in_order


def get_min_location(input_file: Path, seed_format: SeedFormat) -> int:
    seeds, maps = parse_input(input_file, seed_format)
    num_seeds = len(seeds)

    log.debug(f"{num_seeds=}")
    log.debug("Seeds: %s", seeds)
    log.debug("Seed gaps: %s", seeds.gaps)
    for mp in maps:
        log.debug("Map: \n%s", mp)
        log.debug("Gaps: %s", mp.gaps)
        log.debug("Full range: %s", mp.full_range)

    # Chaining the pass through the maps
    res = seeds
    for _map in maps:
        res = _map.apply(res)

    min_location = min(r.first for r in res.ranges)

    log.debug(f"{min_location=}")
    return min_location


def solve_first(input_file: Path) -> str | None:
    return str(get_min_location(input_file, SeedFormat.PLAIN))


def solve_second(input_file: Path) -> str | None:
    return str(get_min_location(input_file, SeedFormat.RANGES))
