from dataclasses import dataclass
import logging
import pdb
import re

from day15.code.visualization import Viz

logger = logging.getLogger(__name__)


def manh(x0, y0, x1, y1):
    return abs(x0 - x1) + abs(y0 - y1)


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y


class Sensor:
    def __init__(self, x, y, beacon_x, beacon_y):
        self.x = int(x)
        self.y = int(y)
        self.beacon = Point(int(beacon_x), int(beacon_y))
        self.dist = manh(self.x, self.y, self.beacon.x, self.beacon.y)

    def __str__(self):
        return f"Sensor at {self.x},{self.y} - located beacon at {self.beacon.x},{self.beacon.y} (dist={self.dist})"

    def within_coverage(self, p):
        return manh(self.x, self.y, p.x, p.y) <= self.dist and not (
            p.x == self.beacon.x and p.y == self.beacon.y
        )

    def perimeter(self):
        points = set()

        x_coords = list(range(self.x - self.dist - 1, self.x + self.dist + 2))

        for x in x_coords:
            # Solve y1 from the manhattan equation
            y = abs(self.x - x) - (self.dist + 1) + self.y
            p = Point(x, y)
            points.add(p)

            y = -abs(self.x - x) + (self.dist + 1) + self.y
            p = Point(x, y)
            points.add(p)

        return points

    def coverage(self):
        points = set()

        x_coords = list(range(self.x - self.dist, self.x + self.dist + 1))
        y_coords = list(range(self.y - self.dist, self.y + self.dist + 1))

        for x in x_coords:
            for y in y_coords:
                if manh(self.x, self.y, x, y) <= self.dist:
                    points.add(Point(x, y))

        return points


def part_one(inp, is_big_input=False):

    if is_big_input:
        y_search = 2000000
        beacon_max_coord = 4000000

    else:
        y_search = 10
        beacon_max_coord = 20

    inp_line_re = re.compile(
        r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)"
    )

    sensors = []

    logger.warning("Parsing input...")
    for line in inp.splitlines():
        match = inp_line_re.match(line)

        sensor_x, sensor_y, beacon_x, beacon_y = match.groups()
        sensor = Sensor(sensor_x, sensor_y, beacon_x, beacon_y)
        sensors.append(sensor)

        logger.info(sensor)

    # Find leftmost and rightmost coverage areas to know the horizontal range to search
    leftmost = min(sensor.x - sensor.dist for sensor in sensors)
    rightmost = max(sensor.x + sensor.dist for sensor in sensors)

    logger.info(f"Leftmost coverage reach at x={leftmost}")
    logger.info(f"Rightmost coverage reach at x={rightmost}")

    coverage_spots = 0

    logger.warning(
        f"Performing coverage search from x={leftmost} to x={rightmost} at row {y_search}"
    )
    for x in range(leftmost, rightmost + 1):
        if any(sensor.within_coverage(Point(x, y_search)) for sensor in sensors):
            coverage_spots += 1

    # Part two
    possible_positions = []

    logger.warning("Computing the perimeter of all sensors")
    # all_perimeters = [sensor.perimeter() for sensor in sensors]

    all_perimeter_points = set()

    for i, sensor in enumerate(sensors):
        perimeter_points = sensor.perimeter()
        logger.info(
            f"Sensor {i}/{len(sensors)} has {len(perimeter_points)} perimeter points"
        )

        perimeter_points = {
            p
            for p in perimeter_points
            if not any(sensor.within_coverage(p) for sensor in sensors)
        }

        # Filter out perimeter points outside hard-set limits (>= 0, <=20 for part one, <=4000000 for part two)
        perimeter_points = {
            p
            for p in perimeter_points
            if p.x >= 0
            and p.x <= beacon_max_coord
            and p.y >= 0
            and p.y <= beacon_max_coord
        }

        # Filter out perimeter points that match other beacons
        perimeter_points = {
            p
            for p in perimeter_points
            if not any(p == sensor.beacon for sensor in sensors)
        }

        logger.info(
            f"After filtering, this sensor has {len(perimeter_points)} perimeter points"
        )

        all_perimeter_points |= perimeter_points

    the_beacon = all_perimeter_points.pop()

    logger.warning(f"The beacon is at {the_beacon}")

    # v = Viz()
    # for sensor in sensors:
    #     # for p in sensor.perimeter():
    #     for p in sensor.coverage():
    #         v.set(p.x, p.y, (0, 0, 255))

    # # for sensor in sensors:
    # #     for p in sensor.perimeter():
    # #         v.set(p.x, p.y, (255, 0, 255))

    # for p in all_perimeter_points:
    #     v.set(p.x, p.y, (255, 255, 0))

    # for sensor in sensors:
    #     v.set(sensor.x, sensor.y, (255, 0, 0))
    #     v.set(sensor.beacon.x, sensor.beacon.y, (0, 255, 0))

    # logger.info(f"{beacon_max_coord=}")
    # for i in range(0, beacon_max_coord + 1):
    #     v.set(i, 0, (255, 255, 255))
    #     v.set(i, beacon_max_coord, (255, 255, 255))
    #     v.set(0, i, (255, 255, 255))
    #     v.set(beacon_max_coord, i, (255, 255, 255))

    # v.run()

    return coverage_spots, the_beacon.x * 4000000 + the_beacon.y


def part_two(inp):
    pass
