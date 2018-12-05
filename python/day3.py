import itertools
import re
from os.path import join, dirname, pardir

INPUT = join(dirname(__file__), pardir, 'input/day3.txt')


def read_input():
    with open(INPUT) as f:
        return [line.strip() for line in f]


def pairs(alist):
    return itertools.combinations(alist, 2)


def parse_claim(claim_str):
    """Parse a line from the input."""
    m = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', claim_str)
    left = int(m.group(2))
    top = int(m.group(3))
    width = int(m.group(4))
    height = int(m.group(5))
    return {
        'id': int(m.group(1)),
        'left': left,
        'right': left + width,
        'top': top,
        'bottom': top + height
    }


def get_overlap(c1, c2):
    """The overlap between two claims, if it exists."""
    width = max(0, min(c1['right'], c2['right']) - max(c1['left'], c2['left']))
    height = max(0, min(c1['bottom'], c2['bottom']) - max(c1['top'], c2['top']))
    left = max(c1['left'], c2['left'])
    top = max(c1['top'], c2['top'])
    if width == 0 or height == 0:
        return None
    return {'left': left, 'right': left + width, 'top': top, 'bottom': top + height}


def list_square_inches(claim):
    """List all square inches in a claim."""
    return [(x, y)
            for x in range(claim['left'], claim['right'])
            for y in range(claim['top'], claim['bottom'])]


def part1():
    claims = [parse_claim(line) for line in read_input()]
    overlapping = set()
    for c1, c2 in pairs(claims):
        overlap = get_overlap(c1, c2)
        if overlap:
            overlapping.update(list_square_inches(overlap))
    answer = len(overlapping)
    return answer


def part2():
    claims = [parse_claim(line) for line in read_input()]

    ids_with_overlap = set()
    for c1, c2 in pairs(claims):
        if get_overlap(c1, c2):
            ids_with_overlap.add(c1['id'])
            ids_with_overlap.add(c2['id'])

    all_ids = set(c['id'] for c in claims)
    answer = all_ids.difference(ids_with_overlap)
    return answer


print('Part 1: ', part1())
print('Part 2: ', part2())
