from os.path import join, dirname, pardir

INPUT = join(dirname(__file__), pardir, 'input/day5.txt')


def read_input():
    with open(INPUT) as f:
        return f.read().strip()


def does_annihilate(u1, u2):
    """Check if two units annihilate each other."""
    if u1 != u2 and u1.lower() == u2.lower():
        return True
    return False


def react_polymer(polymer):
    reacted = []
    for unit in polymer:
        if not reacted:
            reacted.append(unit)
        else:
            if does_annihilate(reacted[-1], unit):
                reacted.pop()
            else:
                reacted.append(unit)
    return reacted


def remove_unit_type(polymer, unit_type):
    """Remove a unit type from a polymer."""
    for unit in polymer:
        if unit.lower() != unit_type:
            yield unit


def part1():
    polymer = read_input()
    answer = len(react_polymer(polymer))
    return answer


def part2():
    polymer = read_input()
    unit_types = set(unit.lower() for unit in polymer)
    lengths = {unit_type: len(react_polymer(remove_unit_type(polymer, unit_type)))
               for unit_type in unit_types}
    answer = min(lengths.values())
    return answer


print('Part 1:', part1())
print('Part 2:', part2())

