import itertools
from os.path import join, dirname, pardir

INPUT = join(dirname(__file__), pardir, 'input/day1.txt')


def read_input():
    with open(INPUT) as f:
        return [int(d) for d in f]


def part1():
    frequency_changes = read_input()
    return sum(frequency_changes)


def part2():
    frequency_changes = read_input()
    current_frequency = 0
    frequencies_seen = set()
    for change in itertools.cycle(frequency_changes):
        current_frequency += change
        if current_frequency in frequencies_seen:
            answer = current_frequency
            return answer

        frequencies_seen.add(current_frequency)


print('Part 1:', part1())
print('Part 2:', part2())
