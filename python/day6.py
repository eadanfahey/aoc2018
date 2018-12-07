from os.path import join, dirname, pardir
from collections import namedtuple, Counter
from operator import itemgetter


INPUT = join(dirname(__file__), pardir, 'input/day6.txt')


Coordinate = namedtuple('Coordinate', ['x', 'y'])


def read_input():
    with open(INPUT) as f:
        return [line.strip() for line in f]


def parse_coordinate(coord_str):
    """Parse a coordinate string from the input."""
    return Coordinate(*map(int, coord_str.split(', ')))


def find_min_bounding_box(coordinates):
    """Find the minimum bounding box which contains all coordinates provided."""
    min_x = min(c.x for c in coordinates)
    min_y = min(c.y for c in coordinates)
    max_x = max(c.x for c in coordinates)
    max_y = max(c.y for c in coordinates)

    return {'top_left': Coordinate(min_x, min_y),
            'bottom_right': Coordinate(max_x, max_y)}


def manhattan_distance(c1, c2):
    """The Manhattan distance between two coordinates."""
    return abs(c1.x - c2.x) + abs(c1.y - c2.y)


def min_all(vals, key):
    """
    The minimum from a set of values. Returns all cases if the minimum is not unique.
    Example: min_all([('a', 2), ('b', 1), ('d', 1)], key=itemgetter(1)) == [('b', 1), ('d', 1)]
    """
    vals_it = iter(vals)
    min_vals = [next(vals_it)]
    for v in vals_it:
        if key(v) < key(min_vals[-1]):
            min_vals = [v]
        elif key(v) == key(min_vals[-1]):
            min_vals.append(v)

    return min_vals


def find_closest(target, candidates):
    """Find the closest coordinate(s) to the target from a list of candidates."""
    distances = ((c, manhattan_distance(c, target)) for c in candidates)
    closest = min_all(distances, key=itemgetter(1))
    return [c[0] for c in closest]


def coordinates_in_box(box):
    """List all coordinates in a box"""
    return [Coordinate(x, y)
            for x in range(box['top_left'].x, box['bottom_right'].x + 1)
            for y in range(box['top_left'].y, box['bottom_right'].y + 1)]


def coordinate_on_edge_of_box(c, box):
    """Check if a coordinate is on the edge of a box."""
    return (c.x == box['top_left'].x or c.x == box['bottom_right'].x or
            c.y == box['top_left'].y or c.y == box['bottom_right'].y)


def part1():

    coordinates = [parse_coordinate(l) for l in read_input()]
    bounding_box = find_min_bounding_box(coordinates)

    # The closest coordinate to each location in the bounding box
    closest = {c: find_closest(c, coordinates) for c in coordinates_in_box(bounding_box)}

    # Find the area corresponding to each coordinate, excluding ones with infinite area
    coordinate_area = Counter()
    for location, closest_coordinate in closest.items():
        # Only keep locations with a unique closest coordinate
        if len(closest_coordinate) == 1:
            coordinate = closest_coordinate[0]
            # Check that area corresponding to the coordinate is not infinite
            if not coordinate_on_edge_of_box(coordinate, bounding_box):
                coordinate_area[coordinate] += 1

    answer = max(coordinate_area.values())
    return answer


def part2():
    coordinates = [parse_coordinate(l) for l in read_input()]
    bounding_box = find_min_bounding_box(coordinates)

    region = []
    for location in coordinates_in_box(bounding_box):
        total_distance = sum(manhattan_distance(location, c) for c in coordinates)
        if total_distance < 10000:
            region.append(location)

    answer = len(region)
    return answer


print('Part 1: ', part1())
print('Part 2: ', part2())
