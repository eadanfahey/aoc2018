import itertools
from os.path import join, dirname, pardir
from collections import Counter

INPUT = join(dirname(__file__), pardir, 'input/day2.txt')


def read_input():
    with open(INPUT) as f:
        return [line.strip() for line in f]


def pairs(alist):
    return itertools.combinations(alist, 2)


def edit_distance(id1, id2):
    return sum(l1 != l2 for l1, l2 in zip(id1, id2))


def part1():
    ids = read_input()
    id_letter_counts = (Counter(id) for id in ids)
    two_times = 0
    three_times = 0
    for id_letter_count in id_letter_counts:
        twice = [l for l, c in id_letter_count.items() if c == 2]
        thrice = [l for l, c in id_letter_count.items() if c == 3]
        if twice:
            two_times += 1
        if thrice:
            three_times += 1

    answer = two_times * three_times
    return answer


def part2():
    ids = read_input()
    for id1, id2 in pairs(ids):
        if edit_distance(id1, id2) == 1:
            return ''.join(l1 for l1, l2 in zip(id1, id2) if l1 == l2)


print('Part 1:', part1())
print('Part 2:', part2())
