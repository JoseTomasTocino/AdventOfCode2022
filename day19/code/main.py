from copy import deepcopy
from enum import Enum, IntEnum
import re
from dataclasses import dataclass
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
    parent_transition: Transition = Transition.INITIAL

    def best_production_prediction(self, bp):
        # In a best-case scenario where we can steadily build a geode robot every turn,
        # in N minutes we would be able to create N robots, but only N-1 of those robots would produce something.
        # The first new robot would be created in turn N and it will produce during N-1 turns
        # The second new robot would be created in turn N+1, and it will produce during N-2 turns
        # Therefore, the sum of the production of the new robots would be the sum of the numbers from N-1 to 1
        # Apply the sum formula (n(n+1)) // 2 and you got it

        return self.resources.geode + (self.minute * self.robots.geode) + ((self.minute - 1) * self.minute) // 2

    def transitions(self, bp: Blueprint):
        transitions = []

        add_wait_transition = True

        # Only build enough ore robots to cover the ore cost of any robot in one turn
        if self.resources.ore >= bp.ore_robot_ore_cost and self.robots.ore < max(
            bp.ore_robot_ore_cost, bp.clay_robot_ore_cost, bp.obsidian_robot_ore_cost, bp.geode_robot_ore_cost
        ):
            transitions.append(Transition.BUILD_ORE_ROBOT)

        # Only build enough clay robots to build an obsidian robot per turn
        if self.resources.ore >= bp.clay_robot_ore_cost and self.robots.clay < bp.obsidian_robot_clay_cost:
            transitions.append(Transition.BUILD_CLAY_ROBOT)

        # If there are no clay robots but there's enough ore to build one, don't wait bro
        if self.resources.ore == bp.clay_robot_ore_cost and self.robots.clay == 0:
            add_wait_transition = False

        # Only build enough obsidian robots to build a geode robot per turn
        if (
            self.resources.ore >= bp.obsidian_robot_ore_cost
            and self.resources.clay >= bp.obsidian_robot_clay_cost
            and self.robots.obsidian < bp.geode_robot_obsidian_cost
        ):
            transitions.append(Transition.BUILD_OBSIDIAN_ROBOT)

        # If there are no obsidian robots but there're enough resources to build one, don't wait bro
        if (
            self.resources.ore >= bp.obsidian_robot_ore_cost
            and self.resources.clay >= bp.obsidian_robot_clay_cost
            and self.robots.obsidian == 0
        ):
            add_wait_transition = False

        if (
            self.resources.ore >= bp.geode_robot_obsidian_cost
            and self.resources.obsidian >= bp.geode_robot_obsidian_cost
        ):
            transitions.append(Transition.BUILD_GEODE_ROBOT)

        # If there are no geode robots but there're enough resources to build one, don't wait bro
        if (
            self.resources.ore >= bp.geode_robot_obsidian_cost
            and self.resources.obsidian >= bp.geode_robot_obsidian_cost
            and self.robots.geode == 0
        ):
            add_wait_transition = False

        # if not transitions:
        if add_wait_transition:
            transitions.append(Transition.WAIT)

        return transitions

    def step(self, bp: Blueprint):
        self.minute -= 1

        mm = bp.max_minutes - self.minute
        ss = "  " * mm

        logger.info(f"{ss}== Minute: {mm}, geodes: {self.resources.geode} ==")
        logger.info(f"{ss}This state comes from transition: {str(self.parent_transition)}")
        logger.info(f"{ss}ore={self.resources.ore}, clay={self.resources.clay}, obsidian={self.resources.obsidian}, geode={self.resources.geode}")
        ## Robot production start

        if self.parent_transition == Transition.BUILD_ORE_ROBOT:
            logger.info(f"{ss}Spend {bp.ore_robot_ore_cost} ore to start building an ore-collecting robot.")
            self.resources.ore -= bp.ore_robot_ore_cost

        elif self.parent_transition == Transition.BUILD_CLAY_ROBOT:
            logger.info(f"{ss}Spend {bp.clay_robot_ore_cost} ore to start building an clay-collecting robot.")
            self.resources.ore -= bp.clay_robot_ore_cost

        elif self.parent_transition == Transition.BUILD_OBSIDIAN_ROBOT:
            logger.info(
                f"{ss}Spend {bp.obsidian_robot_ore_cost} ore and {bp.obsidian_robot_clay_cost} clay to start building an obsidian-collecting robot."
            )
            self.resources.ore -= bp.obsidian_robot_ore_cost
            self.resources.clay -= bp.obsidian_robot_clay_cost

        elif self.parent_transition == Transition.BUILD_GEODE_ROBOT:
            logger.info(
                f"{ss}Spend {bp.geode_robot_ore_cost} ore and {bp.geode_robot_obsidian_cost} obsidian to start building a geode-collecting robot."
            )
            self.resources.ore -= bp.geode_robot_ore_cost
            self.resources.obsidian -= bp.geode_robot_obsidian_cost

        ## Resource production

        if self.robots.ore > 0:
            self.resources.ore += self.robots.ore
            logger.info(
                f"{ss}{self.robots.ore} ore-collecting robots collect {self.robots.ore} ore; you now have {self.resources.ore} ore."
            )

        if self.robots.clay > 0:
            self.resources.clay += self.robots.clay
            logger.info(
                f"{ss}{self.robots.clay} clay-collecting robots collect {self.robots.clay} clay; you now have {self.resources.clay} clay."
            )

        if self.robots.obsidian > 0:
            self.resources.obsidian += self.robots.obsidian
            logger.info(
                f"{ss}{self.robots.obsidian} obsidian-collecting robots collect {self.robots.obsidian} obsidian; you now have {self.resources.obsidian} obsidian."
            )

        if self.robots.geode > 0:
            self.resources.geode += self.robots.geode
            logger.info(
                f"{ss}{self.robots.geode} geode-collecting robots collect {self.robots.geode} geode; you now have {self.resources.geode} geode."
            )

        ## Robot production end

        if self.parent_transition == Transition.BUILD_ORE_ROBOT:
            self.robots.ore += 1
            logger.info(f"{ss}The new ore-collecting robot is ready; you now have {self.robots.ore} of them")

        elif self.parent_transition == Transition.BUILD_CLAY_ROBOT:
            self.robots.clay += 1
            logger.info(f"{ss}The new clay-collecting robot is ready; you now have {self.robots.clay} of them")

        elif self.parent_transition == Transition.BUILD_OBSIDIAN_ROBOT:
            self.robots.obsidian += 1
            logger.info(f"{ss}The new obsidian-collecting robot is ready; you now have {self.robots.obsidian} of them")

        elif self.parent_transition == Transition.BUILD_GEODE_ROBOT:
            self.robots.geode += 1
            logger.info(f"{ss}The new geode-collecting robot is ready; you now have {self.robots.geode} of them")


def part_one(inp):
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
            max_minutes=24,
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

    bp: Blueprint
    for bp in blueprints:
        logger.info(f"Processing blueprint {bp.number}")
        initial_state = State(resources=ResourceCollection(), robots=ResourceCollection(ore=1), minute=24)

        # USE DFS WITHOUT RECURSION TO TRAVERSE THE STATE TREE
        # list nodes_to_visit = {root};
        # while( nodes_to_visit isn't empty ) {
        #   currentnode = nodes_to_visit.take_first();
        #   nodes_to_visit.prepend( currentnode.children );
        #   //do something
        # }

        max_geodes = 0

        to_visit = [(0, initial_state)]

        while to_visit:
            logger.info("")

            depth, cs = to_visit.pop(0)

            cs.step(bp)

            max_geodes = max(max_geodes, cs.resources.geode)

            # Ignore this path if it would be impossible to get a better production than we already have
            if max_geodes >= cs.best_production_prediction(bp):
                logger.info("Ignoring branch, can't reach a better result than current max")
                continue

            # # Ignore branch if there are no geode bots and there's no time to get the obsidian for it
            # if cs.robots.geode == 0 and (cs.minute - 1) < bp.geode_robot_obsidian_cost // cs.robots.obsidian:
            #     continue
            
            if cs.minute == 0:
                logger.info(f"Max minutes reached")
                continue

            transitions = cs.transitions(bp)

            # What if we only consider the best transition and drop the rest?
            transitions = list(sorted(transitions))
            logger.info(f"Possible transitions: {transitions}")
            # new_state: State = deepcopy(current_state)
            # new_state.parent_transition = transitions[0]
            # to_visit.insert(0, (depth + 1, new_state))

            for t in transitions:
                new_state: State = deepcopy(cs)
                new_state.parent_transition = t
                to_visit.insert(0, (depth + 1, new_state))

        blueprint_qualities[bp.number] = bp.number * max_geodes

    return sum(blueprint_qualities.values())


def part_two(inp):
    pass
