#include <iostream>
#include <map>
#include <stack>
#include <vector>
#include <boost/algorithm/string.hpp>
#include <regex>
#include <cmath>

enum Element
{
    Ore,
    Clay,
    Obsidian,
    Geode
};

struct Task
{
    enum TaskType
    {
        None,
        BuildOreRobot,
        BuildClayRobot,
        BuildObsidianRobot,
        BuildGeodeRobot,
        Wait
    };
    TaskType type;
    uint16_t duration;

    Task(TaskType t = TaskType::None, uint16_t m = 0) : type(t), duration(m)
    {
    }

    std::string toString()
    {
        std::string typeStr;

        if (type == TaskType::None)
            typeStr = "None";
        if (type == TaskType::BuildOreRobot)
            typeStr = "BuildOreRobot";
        if (type == TaskType::BuildClayRobot)
            typeStr = "BuildClayRobot";
        if (type == TaskType::BuildObsidianRobot)
            typeStr = "BuildObsidianRobot";
        if (type == TaskType::BuildGeodeRobot)
            typeStr = "BuildGeodeRobot";
        if (type == TaskType::Wait)
            typeStr = "Wait";

        return typeStr + " - " + std::to_string(duration);
    }
};

struct Blueprint
{
    uint16_t id;
    uint16_t maxMinutes;

    uint16_t oreRobotCost;
    uint16_t clayRobotCost;
    uint16_t obsidianRobotOreCost;
    uint16_t obsidianRobotClayCost;
    uint16_t geodeRobotOreCost;
    uint16_t geodeRobotObsidianCost;
};

struct State
{
    uint16_t minute = 1;
    uint16_t resources[4];
    uint16_t robots[4];
    Task task;

    std::vector<Task> path;

    State()
    {
        resources[Element::Ore] = 0;
        resources[Element::Clay] = 0;
        resources[Element::Obsidian] = 0;
        resources[Element::Geode] = 0;

        robots[Element::Ore] = 1;
        robots[Element::Clay] = 0;
        robots[Element::Obsidian] = 0;
        robots[Element::Geode] = 0;
    }

    void startTask(const Blueprint &bp)
    {
        if (task.type == Task::TaskType::BuildOreRobot)
        {
            std::cout << "Starting task: BuildOreRobot \n";
            resources[Element::Ore] -= bp.oreRobotCost;
        }

        else if (task.type == Task::TaskType::BuildClayRobot)
        {
            std::cout << "Starting task: BuildClayRobot \n";
            resources[Element::Ore] -= bp.clayRobotCost;
        }

        else if (task.type == Task::TaskType::BuildObsidianRobot)
        {
            std::cout << "Starting task: BuildObsidianRobot \n";
            resources[Element::Ore] -= bp.obsidianRobotOreCost;
            resources[Element::Clay] -= bp.obsidianRobotClayCost;
        }

        else if (task.type == Task::TaskType::BuildGeodeRobot)
        {
            std::cout << "Starting task: BuildGeodeRobot \n";
            resources[Element::Ore] -= bp.geodeRobotOreCost;
            resources[Element::Obsidian] -= bp.geodeRobotObsidianCost;
        }
    }

    void collectResources()
    {
        resources[Element::Ore] += robots[Element::Ore];
        resources[Element::Clay] += robots[Element::Clay];
        resources[Element::Obsidian] += robots[Element::Obsidian];
        resources[Element::Geode] += robots[Element::Geode];
    }

    void endTask(const Blueprint &bp)
    {
        if (task.type == Task::TaskType::BuildOreRobot)
        {
            std::cout << "Finishing task:BuildOreRobot \n";
            robots[Element::Ore]++;
        }

        else if (task.type == Task::TaskType::BuildClayRobot)
        {
            std::cout << "Finishing task:BuildClayRobot \n";
            robots[Element::Clay]++;
        }

        else if (task.type == Task::TaskType::BuildObsidianRobot)
        {
            std::cout << "Finishing task:BuildObsidianRobot \n";
            robots[Element::Obsidian]++;
        }

        else if (task.type == Task::TaskType::BuildGeodeRobot)
        {
            std::cout << "Finishing task:BuildGeodeRobot \n";
            robots[Element::Geode]++;
        }
    }

    State advanceTo(Task t)
    {
        State newState = *this;

        newState.minute += t.duration;
        newState.task = t;
        newState.path.push_back(task);

        for (int i = 0; i < t.duration - 1; ++i)
            newState.collectResources();

        return newState;
    }

    std::vector<Task> tasks(const Blueprint &bp)
    {
        std::vector<Task> container;

        if (robots[Element::Ore] < std::max({bp.oreRobotCost, bp.clayRobotCost, bp.obsidianRobotOreCost, bp.geodeRobotOreCost}))
        {
            uint16_t waitTime = std::ceil(std::max({0, bp.oreRobotCost - resources[Element::Ore]}) / float(robots[Element::Ore]));
            waitTime = std::max(waitTime, (uint16_t)0) + 1;

            if (minute + waitTime <= bp.maxMinutes)
            {
                container.push_back(Task(Task::TaskType::BuildOreRobot, waitTime));
            }
        }

        if (robots[Element::Clay] < bp.obsidianRobotClayCost)
        {
            uint16_t waitTime = std::ceil(std::max({0, bp.clayRobotCost - resources[Element::Ore]}) / float(robots[Element::Ore]));
            waitTime = std::max(waitTime, (uint16_t)0) + 1;

            if (minute + waitTime <= bp.maxMinutes)
            {
                container.push_back(Task(Task::TaskType::BuildClayRobot, waitTime));
            }
        }

        if (robots[Element::Obsidian] < bp.geodeRobotObsidianCost && robots[Element::Clay] > 0)
        {
            uint16_t waitTime = std::max({std::ceil(std::max({0, bp.obsidianRobotOreCost - resources[Element::Ore]}) / float(robots[Element::Ore])),
                                          std::ceil(std::max({0, bp.obsidianRobotClayCost - resources[Element::Clay]}) / float(robots[Element::Clay]))});
            waitTime = std::max(waitTime, (uint16_t)0) + 1;

            if (minute + waitTime <= bp.maxMinutes)
            {
                container.push_back(Task(Task::TaskType::BuildObsidianRobot, waitTime));
            }
        }

        if (robots[Element::Obsidian] > 0)
        {
            uint16_t waitTime = std::max({std::ceil(std::max({0, bp.geodeRobotOreCost - resources[Element::Ore]}) / float(robots[Element::Ore])),
                                          std::ceil(std::max({0, bp.geodeRobotObsidianCost - resources[Element::Obsidian]}) / float(robots[Element::Obsidian]))});
            waitTime = std::max(waitTime, (uint16_t)0) + 1;

            if (minute + waitTime < bp.maxMinutes)
            {
                container.push_back(Task(Task::TaskType::BuildGeodeRobot, waitTime));
            }
        }

        if (0) {
            if (container.size() == 0)
            {
                container.push_back(Task(Task::TaskType::Wait, bp.maxMinutes - minute));
            }
            
            if (minute == 1){
                container.clear();
                container.push_back(Task(Task::TaskType::BuildClayRobot, 2));
            }

            else if (minute == 3){
                container.clear();
                container.push_back(Task(Task::TaskType::BuildClayRobot, 2));
            }

            else if (minute == 5){
                container.clear();
                container.push_back(Task(Task::TaskType::BuildClayRobot, 2));
            }

            else if (minute == 7){
                container.clear();
                container.push_back(Task(Task::TaskType::BuildObsidianRobot, 4));
            }

            else if (minute == 11){
                container.clear();
                container.push_back(Task(Task::TaskType::BuildClayRobot, 1));
            }

            else if (minute == 12){
                container.clear();
                container.push_back(Task(Task::TaskType::BuildObsidianRobot, 3));
            }

            else if (minute == 15){
                container.clear();
                container.push_back(Task(Task::TaskType::BuildGeodeRobot, 3));
            }

            else if (minute == 18){
                container.clear();
                container.push_back(Task(Task::TaskType::BuildGeodeRobot, 3));
            }

            else if (minute == 21)
            {
                container.clear();
                container.push_back(Task(Task::TaskType::Wait, 3));
            }
        }

        return container;
    }

    uint32_t maxProductionPrediction(const Blueprint &bp)
    {
        uint16_t remainingTurns = bp.maxMinutes - minute;

        return (
            resources[Element::Geode] + (remainingTurns * robots[Element::Geode]) + ((remainingTurns - 1) * remainingTurns) // 2
        );
    }
};

int main()
{
    // Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    std::string line;
    std::regex re{"\\s*Blueprint (\\d+): Each ore robot costs (\\d+) ore. Each clay robot costs (\\d+) ore. Each obsidian robot costs (\\d+) ore and (\\d+) clay. Each geode robot costs (\\d+) ore and (\\d+) obsidian.\\s*"};
    std::map<uint16_t, uint16_t> resultContainer;

    while (std::getline(std::cin, line))
    {
        std::cout << "Processing line: " << line << "\n";
        std::smatch match;

        if (!std::regex_match(line, match, re))
        {
            std::cerr << "Error when applying regular expression to line: " << line << "\n";
            return -1;
        }

        Blueprint bp;

        bp.id = std::stoi(match[1]);
        bp.oreRobotCost = std::stoi(match[2]);
        bp.clayRobotCost = std::stoi(match[3]);
        bp.obsidianRobotOreCost = std::stoi(match[4]);
        bp.obsidianRobotClayCost = std::stoi(match[5]);
        bp.geodeRobotOreCost = std::stoi(match[6]);
        bp.geodeRobotObsidianCost = std::stoi(match[7]);

        std::cout << "bp.id = " << bp.id << "\n";
        std::cout << "bp.oreRobotCost = " << bp.oreRobotCost << "\n";
        std::cout << "bp.clayRobotCost = " << bp.clayRobotCost << "\n";
        std::cout << "bp.obsidianRobotOreCost = " << bp.obsidianRobotOreCost << "\n";
        std::cout << "bp.obsidianRobotClayCost = " << bp.obsidianRobotClayCost << "\n";
        std::cout << "bp.geodeRobotOreCost = " << bp.geodeRobotOreCost << "\n";
        std::cout << "bp.geodeRobotObsidianCost = " << bp.geodeRobotObsidianCost << "\n";

        bp.maxMinutes = 24;

        State initial;

        std::stack<State> stateStack;
        stateStack.push(initial);

        uint16_t maxGeodes = 0;
        
       

        while (stateStack.size() > 0)
        {
            State current = stateStack.top();
            stateStack.pop();

            std::cout << "\n";
            std::cout << "Considering state at minute = " << current.minute << ", task: " << current.task.toString() << "\n";

            current.startTask(bp);
            current.collectResources();
            current.endTask(bp);

            std::cout << "RES: ore=" << current.resources[Element::Ore] << ", clay=" << current.resources[Element::Clay] << ", obsidian=" << current.resources[Element::Obsidian] << ", geode=" << current.resources[Element::Geode] << "\n";
            std::cout << "ROB: ore=" << current.robots[Element::Ore] << ", clay=" << current.robots[Element::Clay] << ", obsidian=" << current.robots[Element::Obsidian] << ", geode=" << current.robots[Element::Geode] << "\n";

            maxGeodes = std::max(maxGeodes, current.resources[Element::Geode]);
            std::cout << "Max geodes= " << maxGeodes << ", max branch prediction=" << current.maxProductionPrediction(bp) << "\n";

            if (maxGeodes > 12)
            {
                for (Task t : current.path)
                {
                    std::cout << t.toString() << "\n";
                }
                throw 5;
            }

            if (maxGeodes > current.maxProductionPrediction(bp))
            {
                std::cout << "Ignoring branch - predicted max for this branch won't get past current max geodes"
                          << "\n";
                continue;
            }

            if (current.minute >= bp.maxMinutes)
            {
                std::cout << "Ignoring branch - max minutes reached"
                          << "\n";
                continue;
            }

            std::cout << "Possible transitions: "
                      << "\n";

            for (Task task : current.tasks(bp))
            {
                auto newState = current.advanceTo(task);
                stateStack.push(newState);
                std::cout << "- minute = " << newState.minute << ", task: " << task.toString()  
                          << ", RES: ore=" << newState.resources[Element::Ore] << ", clay=" << newState.resources[Element::Clay] << ", obsidian=" << newState.resources[Element::Obsidian] << ", geode=" << newState.resources[Element::Geode]
                          << ", ROB: ore=" << newState.robots[Element::Ore] << ", clay=" << newState.robots[Element::Clay] << ", obsidian=" << newState.robots[Element::Obsidian] << ", geode=" << newState.robots[Element::Geode] << "\n";
            }
        }

        std::cout << "FINAL - Max geodes for bp id=" << bp.id << " => " << maxGeodes << "\n\n\n";
        resultContainer[bp.id] = maxGeodes;
    }

    uint16_t res = 0;

    for (auto pair: resultContainer)
    {
        std::cout << pair.first << ": " << pair.second << "\n";
        res += pair.first * pair.second;
    }

    std::cout << res << std::endl;
}
