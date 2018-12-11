import numpy as np
from operator import itemgetter


SERIAL_NUMBER = 9798
WIDTH = 300


def nth_digit(i, n):
    """The n-th decimal digit of the number i."""
    digit = 0
    for _ in range(n + 1):
        digit = i % 10
        i = int(i / 10)
    return digit


def fuel_cell_power(x, y):
    rack_id = x + 10
    return nth_digit(((rack_id * y) + SERIAL_NUMBER) * rack_id, 2) - 5


def cell_grid():
    return np.array([[fuel_cell_power(x, y) for x in range(WIDTH)] for y in range(WIDTH)])


def convolution(grid, size):
    for y in range(WIDTH - size + 1):
        for x in range(WIDTH - size + 1):
            subgrid = grid[y:(y+size), x:(x+size)]
            yield {
                'top_left': (x, y),
                'total_power': subgrid.sum()
            }


def part1():
    grid = cell_grid()
    max_power = max(convolution(grid, 3), key=itemgetter('total_power'))
    return max_power['top_left']


def part2():
    grid = cell_grid()
    max_power_size = {}
    for size in range(WIDTH):
        max_power_size[size] = max(convolution(grid, size), key=itemgetter('total_power'))
    max_power = max(max_power_size.items(), key=lambda k: k[1]['total_power'])
    return max_power[1]['top_left'], max_power[0]


print('Part 1:', part1())
print('Part 2:', part2())
