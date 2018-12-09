import itertools
from collections import Counter, deque


def play_game(num_players, last_marble):
    # Represent the circle as a deque. It's last element is the current position
    circle = deque([0])
    scores = Counter()
    players = list(range(1, num_players + 1))
    marbles = range(1, last_marble + 1)
    for player, marble in zip(itertools.cycle(players), marbles):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[player] += circle.pop() + marble
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores.values())


def part1():
    num_players = 448
    last_marble = 71628
    return play_game(num_players, last_marble)


def part2():
    num_players = 448
    last_marble = 71628 * 100
    return play_game(num_players, last_marble)


print('Part 1:', part1())
print('Part 2:', part2())
