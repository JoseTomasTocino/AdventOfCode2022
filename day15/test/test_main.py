import logging
import os.path
from ..code.main import Sensor, part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

# sample_input = """Sensor at x=15, y=5: closest beacon is at x=17, y=8"""

# def test_coverage(caplog):
#     caplog.set_level(logging.INFO)

#     s = Sensor(8, 7, 2, 10)

#     assert s.within_coverage(1, 7)
#     assert s.within_coverage(8, 0)
#     assert not s.within_coverage(2, 10)
#     assert not s.within_coverage(20, 20)


# def test_perimeter(caplog):
#     caplog.set_level(logging.INFO)

#     s = Sensor(10, 10, 10, 7)
#     perimeter = s.perimeter()

#     logger.info(f"Perimeter: {perimeter}")


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    # assert part_one(sample_input, False) == (26, 56000011)
    # assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.WARNING)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content, True) == 5299855
        # assert part_two(content) == None
