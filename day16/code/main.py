from copy import deepcopy
from dataclasses import dataclass
import re
import logging

from day16.code.dijkstra import Graph

logger = logging.getLogger(__name__)

MAX_MINUTES = 30


@dataclass
class Valve:
    name: str
    flow: int
    neighbors: list
    open: bool = False
    visited: bool = False


def get_best_approach(
    graph, minutes, released_pressure, valves, open_valves, current, path
):
    logger.info(
        f"{'  '* (MAX_MINUTES - minutes)}Minutes: {minutes}, {current=}, path: {path}, {released_pressure=}"
    )

    # If all valves are alredy open, just consume the remaining time releasing pressure
    if all(v.open for v in valves.values()):
        logger.info(f"{'  '* (MAX_MINUTES - minutes)}All valves are open, just wait")
        released_pressure += minutes * sum(v.flow for v in valves.values() if v.open)
        minutes = 0

    if minutes <= 0:
        logger.info(
            f"{'  '* (MAX_MINUTES - minutes)}END OF MINUTES, {released_pressure=}, {current=} ##################################################"
        )
        return released_pressure

    valve = valves[current]
    valve.visited = True

    approaches = []

    # First, consider the approach of not moving anymore
    approaches.append(
        released_pressure + minutes * sum(v.flow for v in valves.values() if v.open)
    )
    logger.info(
        f"{'  '* (MAX_MINUTES - minutes)}If we don't move anymore, total released pressure when time ends would be: {approaches[-1]}"
    )

    # # Update released pressure according to open valves
    # local_pressure = sum(v.flow for v in valves.values() if v.open)
    # released_pressure += local_pressure

    closed_valves = [
        v.name for v in valves.values() if not v.open and v.name != current
    ]
    distances = graph.dijkstra(current)

    valves_with_throughput = []

    for cv in closed_valves:
        cost_to_reach_and_open = distances[cv] + 1
        throughput = (minutes - cost_to_reach_and_open) * valves[cv].flow
        logger.info(
            f"{'  '* (MAX_MINUTES - minutes)}Distance from {current} to {cv} is {distances[cv]} minutes + 1 to open the valve = {cost_to_reach_and_open}, throughput: {throughput}"
        )

        valves_with_throughput.append((cv, throughput))

    valves_with_throughput = list(
        sorted(valves_with_throughput, key=lambda x: x[1], reverse=True)
    )

    for cv, throughput in valves_with_throughput:

        if throughput <= 0:
            continue

        local_cost = distances[cv] + 1

        local_minutes = minutes - local_cost

        local_valves = deepcopy(valves)
        local_valves[cv].open = True

        local_open_valves = deepcopy(open_valves)
        local_open_valves.add(cv)

        local_pressure = released_pressure + local_cost * sum(
            v.flow for v in valves.values() if v.open
        )

        if local_minutes < 0:
            logger.info(
                f"{'  '* (MAX_MINUTES - minutes)}Can't travel to {cv}, not enough time."
            )
            continue

        logger.info(
            f"{'  '* (MAX_MINUTES - minutes)}Decision: travel to {cv} and open it, cost: {local_cost}"
        )

        approaches.append(
            get_best_approach(
                graph,
                local_minutes,
                local_pressure,
                local_valves,
                local_open_valves,
                cv,
                path + [current],
            )
        )

    if approaches:
        return max(approaches)

    else:
        return 0


def get_best_approach_with_elephant(
    graph, minutes, released_pressure, valves, open_valves, current, current_elephant, path
):
    logger.info(
        f"{'  '* (MAX_MINUTES - minutes)}Minutes: {minutes}, {current=}, {current_elephant=}, path: {path}, {released_pressure=}"
    )

    ################################################################################################################################################
    ################################################################################################################################################
    # If all valves are alredy open, just consume the remaining time releasing pressure
    if all(v.open for v in valves.values()):
        logger.info(f"{'  '* (MAX_MINUTES - minutes)}All valves are open, just wait")
        released_pressure += minutes * sum(v.flow for v in valves.values() if v.open)
        minutes = 0

    if minutes <= 0:
        logger.info(
            f"{'  '* (MAX_MINUTES - minutes)}END OF MINUTES, {released_pressure=}, {current=} ##################################################"
        )
        return released_pressure

    ################################################################################################################################################

    valve = valves[current]
    valve.visited = True

    approaches = []

    ################################################################################################################################################
    # First, consider the approach of not moving anymore for the remaining minutes

    approaches.append(
        released_pressure + minutes * sum(v.flow for v in valves.values() if v.open)
    )
    logger.info(
        f"{'  '* (MAX_MINUTES - minutes)}If we don't move anymore, total released pressure when time ends would be: {approaches[-1]}"
    )

    ################################################################################################################################################


    closed_valves = [
        v.name for v in valves.values() if not v.open and v.name != current
    ]
    distances = graph.dijkstra(current)
    
    valves_with_throughput = [(cv, valves[cv].flow * (minutes - distances[cv] - 1)) for cv in closed_valves]
    valves_with_throughput = sorted(valves_with_throughput, key=lambda x: x[1], reverse=True)

    current_me = current
    current_elephant = current

    destination_me = valves_with_throughput[0][0]
    destination_elephant = valves_with_throughput[1][0]

    remaining_steps_me = distances[destination_me] + 1
    remaining_steps_elephant = distances[destination_elephant] + 1

    logger.info(f"Initial destination for me: {destination_me}, cost: {remaining_steps_me}")
    logger.info(f"Initial destination for elephant: {destination_elephant}, cost: {remaining_steps_elephant}")

    while minutes > 1:
        released_pressure += sum(v.flow for v in valves.values() if v.open)

        remaining_steps_me -= 1
        remaining_steps_elephant -= 1
        minutes -= 1

        logger.info(f"Minutes: {minutes}")

        if remaining_steps_me == 0:
            logger.info(f"I reached destination {destination_me}")

            # Update reached destination
            valves[destination_me].open = True
            open_valves.add(destination_me)            

            # Get a new destination
            distances = graph.dijkstra(current_me)

            closed_valves = [
                v.name for v in valves.values() if not v.open and v.name != current_me and v.name != destination_elephant
            ]
            
            valves_with_throughput = [(cv, valves[cv].flow * (minutes - distances[cv] - 1)) for cv in closed_valves]
            valves_with_throughput = sorted(valves_with_throughput, key=lambda x: x[1], reverse=True)

            if valves_with_throughput:
                destination_me = valves_with_throughput[0][0]
                remaining_steps_me = distances[destination_me] + 1

                logger.info(f"I received a new destination: {destination_me}, cost: {remaining_steps_me}")

        if remaining_steps_elephant == 0:
            logger.info(f"Elephant reached destination {destination_elephant}")

            # Update reached destination
            valves[destination_elephant].open = True
            open_valves.add(destination_elephant)

            # Get a new destination
            distances = graph.dijkstra(current_elephant)

            closed_valves = [
                v.name for v in valves.values() if not v.open and v.name != current_elephant and v.name != destination_me
            ]
            
            valves_with_throughput = [(cv, valves[cv].flow * (minutes - distances[cv] - 1)) for cv in closed_valves]
            valves_with_throughput = sorted(valves_with_throughput, key=lambda x: x[1], reverse=True)

            if valves_with_throughput:
                destination_elephant = valves_with_throughput[0][0]
                remaining_steps_elephant = distances[destination_elephant] + 1

                logger.info(f"Elephant received a new destination: {destination_elephant}, cost: {remaining_steps_elephant}")

    return released_pressure



        

    
    # for cv, throughput in valves_with_throughput:
    #     logger.info((cv, throughput))

    #     if throughput <= 0:
    #         continue

        # local_cost = distances[cv] + 1

        # local_minutes = minutes - local_cost

        # local_valves = deepcopy(valves)
        # local_valves[cv].open = True

        # local_open_valves = deepcopy(open_valves)
        # local_open_valves.add(cv)

        # local_pressure = released_pressure + local_cost * sum(
        #     v.flow for v in valves.values() if v.open
        # )

        # if local_minutes < 0:
        #     logger.info(
        #         f"{'  '* (MAX_MINUTES - minutes)}Can't travel to {cv}, not enough time."
        #     )
        #     continue

        # logger.info(
        #     f"{'  '* (MAX_MINUTES - minutes)}Decision: travel to {cv} and open it, cost: {local_cost}"
        # )

        # approaches.append(
        #     get_best_approach(
        #         graph,
        #         local_minutes,
        #         local_pressure,
        #         local_valves,
        #         local_open_valves,
        #         cv,
        #         path + [current],
        #     )
        # )

    if approaches:
        return max(approaches)

    else:
        return 0


def bootstrap(inp, use_elephant):
    valve_re = re.compile(
        r"Valve ([A-Z]+?) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
    )

    valves = {}

    graph = Graph(len(inp.splitlines()))

    logger.info(f"Parsing input, there are {graph.v} vertices...")

    for line in inp.splitlines():
        match = valve_re.match(line)

        # Read valve parameters
        valve_name = match.group(1)
        valve_flow = int(match.group(2))
        valve_neighbours = [x.strip() for x in match.group(3).split(",")]

        # Build valve
        valve = Valve(valve_name, valve_flow, valve_neighbours)
        valves[valve_name] = valve

        # Add valve to graph
        for n in valve_neighbours:
            graph.add_edge(valve_name, n)
            graph.add_edge(n, valve_name)

        logger.info(valve)

    starting_valve = "AA"
    minutes = MAX_MINUTES

    logger.info("")

    if use_elephant:
        return get_best_approach_with_elephant(graph, minutes, 0, valves, set(), starting_valve, starting_valve, [])
    else:
        return get_best_approach(graph, minutes, 0, valves, set(), starting_valve, [])


def part_one(inp):
    return bootstrap(inp, False)


def part_two(inp):
    return bootstrap(inp, True)
