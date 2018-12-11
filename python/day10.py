import re
from os.path import join, dirname, pardir
from collections import namedtuple


INPUT = join(dirname(__file__), pardir, 'input/day10.txt')

Vector = namedtuple('Vector', ['x', 'y'])


def read_input():
    with open(INPUT) as f:
        return [line.strip() for line in f]


def parse_point(point_str):
    m = re.match(
        r'position=<(\s*-?[0-9]+),(\s*-?[0-9]+)> velocity=<(\s*-?[0-9]+),(\s*-?[0-9]+)>',
        point_str
    )
    return {
        'position': Vector(int(m.group(1)), int(m.group(2))),
        'velocity': Vector(int(m.group(3)), int(m.group(4)))
    }


def min_bounding_box(pos_vectors):
    min_x = min(p.x for p in pos_vectors)
    min_y = min(p.y for p in pos_vectors)
    max_x = max(p.x for p in pos_vectors)
    max_y = max(p.y for p in pos_vectors)
    return {
        'top_left': Vector(min_x, min_y),
        'bottom_right': Vector(max_x, max_y)
    }


def width(box):
    top_left, bottom_right = box['top_left'], box['bottom_right']
    return abs(bottom_right.x - top_left.x)


def height(box):
    top_left, bottom_right = box['top_left'], box['bottom_right']
    return abs(bottom_right.y - top_left.y)


def area(box):
    return height(box) * width(box)


def iterate(point):
    pos, vel = point['position'], point['velocity']
    return {
        'position': Vector(pos.x + vel.x, pos.y + vel.y),
        'velocity': vel
    }


def draw(positions):
    b = min_bounding_box(positions)
    x0, y0 = b['top_left'].x, b['top_left'].y
    translated = [Vector(p.x - x0, p.y - y0) for p in positions]
    grid = [[' '] * (width(b) + 1) for _ in range(height(b) + 1)]
    for p in translated:
        grid[p.y][p.x] = '#'

    print('\n'.join(''.join(r) for r in grid))


def part1_and_2():
    # points = [parse_point(s) for s in read_input()]
    # for i in range(11000):
    #     points = [iterate(p) for p in points]
    #     positions = [p['position'] for p in points]
    #     b = min_bounding_box(positions)
    #     print(i, area(b))

    # Manually inspection above indicates bounding box has smallest
    # area after 10011 seconds. The message likely appears then

    points = [parse_point(s) for s in read_input()]
    positions = None
    for i in range(10011):
        points = [iterate(p) for p in points]
        positions = [p['position'] for p in points]

    draw(positions)
