from copy import deepcopy
from enum import Enum, IntEnum
from functools import reduce
from math import ceil
import operator
import re
from dataclasses import dataclass, field
from collections import namedtuple
import logging

logger = logging.getLogger(__name__)


@dataclass
class Blueprint:
    number: int
    max_minutes: int

    ore_robot_ore_cost: int

    clay_robot_ore_cost: int

    obsidian_robot_ore_cost: int
    obsidian_robot_clay_cost: int

    geode_robot_ore_cost: int
    geode_robot_obsidian_cost: int


class Transition(IntEnum):
    INITIAL = 0
    WAIT = 1
    BUILD_ORE_ROBOT = 2
    BUILD_CLAY_ROBOT = 3
    BUILD_OBSIDIAN_ROBOT = 4
    BUILD_GEODE_ROBOT = 5


@dataclass(unsafe_hash=True)
class ResourceCollection:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


@dataclass(unsafe_hash=True)
class State:
    resources: ResourceCollection
    robots: ResourceCollection
    minute: int
    path: list = field(default_factory=list)
    parent_transition: Transition = Transition.INITIAL
    depth: int = 0

    def best_production_prediction(self, bp: Blueprint):
        # In a best-case scenario where we can steadily build a geode robot every turn,
        # in N minutes we would be able to create N robots, but only N-1 of those robots would produce something.
        # The first new robot would be created in turn N and it will produce during N-1 turns
        # The second new robot would be created in turn N+1, and it will produce during N-2 turns
        # Therefore, the sum of the production of the new robots would be the sum of the numbers from N-1 to 1
        # Apply the sum formula (n(n+1)) // 2 and you got it

        remaining_turns = bp.max_minutes - self.minute

        return (
            self.resources.geode
            + (remaining_turns * self.robots.geode)
            + ((remaining_turns - 1) * remaining_turns) // 2
        )

    def apply_transition(self, wait_time: int, transition: Transition, bp: Blueprint):
        # logger.info(f"Applying transition {str(transition)}, {wait_time=}")
        new = deepcopy(self)
        new.depth += 1
        new.parent_transition = transition
        new.path.append((new.minute, transition))
        new.minute += wait_time

        new.resources.ore += new.robots.ore * wait_time
        new.resources.clay += new.robots.clay * wait_time
        new.resources.obsidian += new.robots.obsidian * wait_time
        new.resources.geode += new.robots.geode * wait_time

        if transition == Transition.BUILD_ORE_ROBOT:
            new.resources.ore -= bp.ore_robot_ore_cost
            new.robots.ore += 1

        elif transition == Transition.BUILD_CLAY_ROBOT:
            new.resources.ore -= bp.clay_robot_ore_cost
            new.robots.clay += 1

        elif transition == Transition.BUILD_OBSIDIAN_ROBOT:
            new.resources.ore -= bp.obsidian_robot_ore_cost
            new.resources.clay -= bp.obsidian_robot_clay_cost
            new.robots.obsidian += 1

        elif transition == Transition.BUILD_GEODE_ROBOT:
            new.resources.ore -= bp.geode_robot_ore_cost
            new.resources.obsidian -= bp.geode_robot_obsidian_cost
            new.robots.geode += 1

        return new

    def transitions(self, bp: Blueprint):
        transitions = []

        # BUILD_ORE_ROBOT transition can always be considered, because you start with an ore robot
        # Only build enough ore robots to cover the ore cost of any robot in one turn
        if self.robots.ore < max(
            bp.ore_robot_ore_cost, bp.clay_robot_ore_cost, bp.obsidian_robot_ore_cost, bp.geode_robot_ore_cost
        ):
            wait_time = ceil((bp.ore_robot_ore_cost - self.resources.ore) / self.robots.ore)
            wait_time = max(wait_time, 0) + 1

            # logger.info(f"Ore robot ore cost: {bp.ore_robot_ore_cost}")
            # logger.info(f"Current ore: {self.resources.ore}")
            # logger.info(f"Current ore robots: {self.robots.ore}")
            # logger.info(f"Wait time: {wait_time}")

            if self.minute + wait_time <= bp.max_minutes:
                transitions.append((wait_time, Transition.BUILD_ORE_ROBOT))

        # BUILD_CLAY_ROBOT transition can always be considered, for the same reason as before
        # Only build enough clay robots to build an obsidian robot per turn
        if self.robots.clay < bp.obsidian_robot_clay_cost:

            wait_time = ceil((bp.clay_robot_ore_cost - self.resources.ore) / self.robots.ore)
            wait_time = max(wait_time, 0) + 1

            # logger.info(f"Clay robot ore cost: {bp.clay_robot_ore_cost}")
            # logger.info(f"Current ore: {self.resources.ore}")
            # logger.info(f"Pending ore to obtain {(bp.clay_robot_ore_cost - self.resources.ore)}"")
            # logger.info(f"Current ore robots: {self.robots.ore}")
            # logger.info(f"Wait time: {wait_time}")

            if self.minute + wait_time <= bp.max_minutes:
                transitions.append((wait_time, Transition.BUILD_CLAY_ROBOT))

        # BUILD_OBSIDIAN_ROBOT transition can only be considered if there's at least one clay robot
        # Only build enough obsidian robots to build a geode robot per turn
        if self.robots.obsidian < bp.geode_robot_obsidian_cost and self.robots.clay > 0:
            wait_time = max(
                ceil((bp.obsidian_robot_ore_cost - self.resources.ore) / self.robots.ore),
                ceil((bp.obsidian_robot_clay_cost - self.resources.clay) / self.robots.clay),
            )
            wait_time = max(wait_time, 0) + 1

            if self.minute + wait_time <= bp.max_minutes:
                transitions.append((wait_time, Transition.BUILD_OBSIDIAN_ROBOT))

        # BUILD_GEODE_ROBOT transition can only be considered if there's at least one obsidian robot
        if self.robots.obsidian > 0:
            wait_time = max(
                ceil((bp.geode_robot_ore_cost - self.resources.ore) / self.robots.ore),
                ceil((bp.geode_robot_obsidian_cost - self.resources.obsidian) / self.robots.obsidian),
            )
            wait_time = max(wait_time, 0) + 1

            # Comparison here is strict-lower-than because there's no point in building a geode robot in the last turn
            if self.minute + wait_time < bp.max_minutes:
                transitions.append((wait_time, Transition.BUILD_GEODE_ROBOT))

        if not transitions:
            transitions.append((1, Transition.WAIT))

        return transitions

    def log(self, bp):
        mm = self.minute
        ss = "  " * self.depth

        logger.info(f"{ss}== Minute: {mm}, geodes: {self.resources.geode} ==")
        logger.info(f"{ss}This state comes from transition: {str(self.parent_transition)}")
        # logger.info(
        #     f"{ss}RES: ore={self.resources.ore}, clay={self.resources.clay}, obsidian={self.resources.obsidian}, geode={self.resources.geode}"
        # )
        # logger.info(
        #     f"{ss}ROB: ore={self.robots.ore}, clay={self.robots.clay}, obsidian={self.robots.obsidian}, geode={self.robots.geode}"
        # )


def solution(inp, max_time=24, multiply_final_geodes=False, limit_blueprints=False):
    blueprints = []

    for bp_raw in inp.splitlines():
        bp_name, bp_body = bp_raw.split(": ")
        _, bp_number = bp_name.split(" ")
        bp_number = int(bp_number)

        costs = bp_body.split(".")

        ore_re = re.compile(r"(\d+) ore")
        clay_re = re.compile(r"(\d+) clay")
        obsidian_re = re.compile(r"(\d+) obsidian")

        bp = Blueprint(
            number=bp_number,
            max_minutes=max_time,
            ore_robot_ore_cost=int(ore_re.search(costs[0]).group(1)),
            clay_robot_ore_cost=int(ore_re.search(costs[1]).group(1)),
            obsidian_robot_ore_cost=int(ore_re.search(costs[2]).group(1)),
            obsidian_robot_clay_cost=int(clay_re.search(costs[2]).group(1)),
            geode_robot_ore_cost=int(ore_re.search(costs[3]).group(1)),
            geode_robot_obsidian_cost=int(obsidian_re.search(costs[3]).group(1)),
        )

        blueprints.append(bp)

    # Simulation
    blueprint_qualities = {}

    if limit_blueprints:
        blueprints = blueprints[:3]

    bp: Blueprint
    for bp in blueprints:
        logger.info(f"Processing blueprint {bp.number}")

        initial_state = State(resources=ResourceCollection(ore=1), robots=ResourceCollection(ore=1), minute=1)

        max_geodes = 0
        max_state = None

        considered_states = 0

        to_visit = [initial_state]

        while to_visit:
            logger.info("")

            state = to_visit.pop(0)
            state.log(bp)
            considered_states += 1

            # state.step(bp)

            if state.resources.geode > max_geodes:
                max_geodes = state.resources.geode
                max_state = state

            logger.info(f"{'  ' * state.depth}Current max: {max_geodes}, predicted branch max: {state.best_production_prediction(bp)}")
            

            # Ignore this path if it would be impossible to get a better production than we already have
            if max_geodes > state.best_production_prediction(bp):
                logger.info(f"{'  ' * state.depth}Ignoring branch, can't reach a better result than current max")
                continue

            if state.minute >= bp.max_minutes:
                logger.info(f"{'  ' * state.depth}Max minutes reached")
                continue

            transitions = sorted(state.transitions(bp), key=lambda x: x[1])
            logger.info(f"{'  ' * state.depth}Possible transitions: {transitions}")

            # forced_transitions = {
            #     1: (2, Transition.BUILD_ORE_ROBOT),
            #     3: (2, Transition.BUILD_ORE_ROBOT),
            #     5: (1, Transition.BUILD_CLAY_ROBOT),
            #     6: (1, Transition.BUILD_CLAY_ROBOT),
            #     7: (1, Transition.BUILD_CLAY_ROBOT),
            #     8: (1, Transition.BUILD_CLAY_ROBOT),
            #     9: (1, Transition.BUILD_CLAY_ROBOT),
            #     10: (1, Transition.BUILD_CLAY_ROBOT),
            #     11: (1, Transition.BUILD_OBSIDIAN_ROBOT),
            #     12: (1, Transition.BUILD_OBSIDIAN_ROBOT),
            #     13: (1, Transition.BUILD_OBSIDIAN_ROBOT),
            #     14: (1, Transition.BUILD_OBSIDIAN_ROBOT),
            #     15: (1, Transition.BUILD_CLAY_ROBOT),
            #     16: (1, Transition.BUILD_OBSIDIAN_ROBOT),
            #     17: (1, Transition.BUILD_GEODE_ROBOT),
            #     18: (1, Transition.BUILD_OBSIDIAN_ROBOT),
            #     19: (1, Transition.BUILD_GEODE_ROBOT),
            #     20: (1, Transition.BUILD_OBSIDIAN_ROBOT),
            #     21: (1, Transition.BUILD_GEODE_ROBOT),
            #     22: (1, Transition.WAIT),
            #     23: (1, Transition.WAIT)
            # }

            # if state.minute in forced_transitions:
            #     transitions = [forced_transitions[state.minute]]

            # if state.minute == 1:
            #     transitions = [(2, Transition.BUILD_CLAY_ROBOT)]

            # elif state.minute == 3:
            #     transitions = [(2, Transition.BUILD_CLAY_ROBOT)]

            # elif state.minute == 5:
            #     transitions = [(2, Transition.BUILD_CLAY_ROBOT)]

            # elif state.minute == 7:
            #     transitions = [(4, Transition.BUILD_OBSIDIAN_ROBOT)]

            # elif state.minute == 11:
            #     transitions = [(1, Transition.BUILD_CLAY_ROBOT)]

            # elif state.minute == 12:
            #     transitions = [(3, Transition.BUILD_OBSIDIAN_ROBOT)]

            # elif state.minute == 15:
            #     transitions = [(3, Transition.BUILD_GEODE_ROBOT)]

            # elif state.minute == 18:
            #     transitions = [(3, Transition.BUILD_GEODE_ROBOT)]

            logger.info(f"{'  ' * state.depth}Possible transitions: {transitions}")

            # pekepeke += 1
            # if pekepeke == 15:
            #     logger.info("PEKEPEKEBREAKING")
            #     break

            for wt, t in transitions:
                new_state: State = state.apply_transition(transition=t, wait_time=wt, bp=bp)
                to_visit.insert(0, new_state)

        blueprint_qualities[bp.number] = max_geodes

    if max_state is not None:
        pass
        logger.info("")
        logger.info(f"Max geode ({max_geodes}) state path:")
        for ff in max_state.path:
            pass
            logger.info(f"  - {ff}")

    logger.warning(f"{considered_states=}")

    if multiply_final_geodes:
        return reduce(operator.mul, blueprint_qualities.values())
    else:
        return sum(i * x for i, x in blueprint_qualities.items())


def part_one(inp):
    return solution(inp, 24, False, True)


def part_two(inp):
    return solution(inp, 32, True)
