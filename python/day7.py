import re
from os.path import join, dirname, pardir
from collections import defaultdict


INPUT = join(dirname(__file__), pardir, 'input/day7.txt')


def read_input():
    with open(INPUT) as f:
        return [line.strip() for line in f]


def parse_instruction(instruction_str):
    m = re.match(r'Step ([A-Z]+) must be finished before step ([A-Z]+) can begin',
                 instruction_str)
    return {
        'dependency': m.group(1),
        'step': m.group(2),
    }


def construct_dependency_graph(instructions):
    """
    Construct the dependency graph from a list of instructions. Represented as a
    doubly-linked list, where the parent and child nodes are provided for each node.
    """
    graph = defaultdict(lambda: {'children': [], 'parents': []})
    for i in instructions:
        step, dependency = i['step'], i['dependency']
        graph[step]['parents'].append(dependency)
        graph[dependency]['children'].append(step)
    return dict(graph)


def get_root_nodes(graph):
    """Find all root nodes in a graph, i.e. nodes with no parents."""
    return [node for node, family in graph.items() if len(family['parents']) == 0]


def is_ready(graph, node, already_done):
    """Check if a node is ready to start working on."""
    return all(p in already_done for p in graph[node]['parents'])


def part1():
    instructions = [parse_instruction(i) for i in read_input()]
    graph = construct_dependency_graph(instructions)

    ready = sorted(get_root_nodes(graph))
    already_done = []
    while ready:
        done = ready[0]
        already_done.append(done)
        new_ready = [n for n in graph[done]['children']
                     if is_ready(graph, n, already_done)]
        ready = sorted(ready[1:] + new_ready)

    answer = ''.join(already_done)
    return answer


def time_to_complete(step):
    """The time to complete a step"""
    return 60 + ord(step.lower()) - ord('a') + 1


def part2():
    num_workers = 5
    instructions = [parse_instruction(i) for i in read_input()]
    graph = construct_dependency_graph(instructions)

    elapsed = 0
    ready = sorted(get_root_nodes(graph))
    already_done = []
    in_progress = dict()
    workers_available = num_workers
    while ready or in_progress:

        # Check if any in-progress steps are complete
        done = [step for step, remaining in in_progress.items() if remaining == 0]
        already_done.extend(done)
        new_ready = []
        for step in done:
            new_ready.extend([n for n in graph[step]['children']
                              if is_ready(graph, n, already_done)])
        ready = sorted(new_ready + [n for n in ready if n not in done])
        workers_available += len(done)
        in_progress = {k: v for k, v in in_progress.items() if k not in done}

        # Assign any available workers, to any steps that are ready
        staged = ready[:workers_available]
        ready = ready[workers_available:]
        workers_available -= len(staged)
        for step in staged:
            in_progress[step] = time_to_complete(step)

        # Decrement the remaining time for each in-progress step
        in_progress = {k: v - 1 for k, v in in_progress.items()}

        elapsed += 1

    return elapsed


print('Part 1:', part1())
print('Part 2:', part2())
