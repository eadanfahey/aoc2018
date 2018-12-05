import itertools
import re
import datetime as dt
from operator import itemgetter
from os.path import join, dirname, pardir
from collections import defaultdict, Counter

INPUT = join(dirname(__file__), pardir, 'input/day4.txt')


def read_input():
    with open(INPUT) as f:
        return [line.strip() for line in sorted(f.readlines())]


def zipper(it):
    """Example: [1, 2, 3, 4] --> (1, 2), (2, 3), (3, 4)"""
    return zip(it, itertools.islice(it, 1, None))


def range_minute(start, end):
    """A range of datetimes from start to end, inclusive, incremented by the minute."""
    d = start
    while d <= end:
        yield d
        d += dt.timedelta(minutes=1)


def get_shifts(input_list):
    """
    A dictionary mapping each guard to a list of their shifts. Each shift is a list of
    events.
    """
    def parse_event(event_str):
        m = re.match(r'\[(\d+-\d+-\d+ \d+:\d+)\] (Guard #(\d+) begins shift|(falls asleep)|(wakes up))',
                     event_str)
        timestamp = dt.datetime.strptime(m.group(1), '%Y-%m-%d %H:%M')
        event = m.group(2)
        guard = None
        if 'begins shift' in event:
            event = 'begins shift'
            guard = int(m.group(3))
        result = {'timestamp': timestamp, 'event': event}
        if guard:
            result['guard'] = guard
        return result

    input_iterator = iter(input_list)
    guard_shifts = defaultdict(list)
    first_event = parse_event(next(input_iterator))
    current_shift = [first_event]
    current_guard = first_event['guard']
    for line in input_iterator:
        event = parse_event(line)
        if event.get('guard'):
            # The shift has changed
            guard_shifts[current_guard].append(current_shift)
            current_guard = event['guard']
            current_shift = []
        current_shift.append(event)

    return guard_shifts


def time_asleep(shift):
    """The time asleep during a shift, in minutes."""
    asleep_minutes = 0
    for prev_event, next_event in zipper(shift):
        if prev_event['event'] == 'falls asleep':
            assert next_event['event'] == 'wakes up'  # assumption about input
            asleep_minutes += (next_event['timestamp'] - prev_event['timestamp']).seconds / 60
    return asleep_minutes


def intervals_asleep(shift):
    """
    List the all intervals, as pairs of timestamps, that a guard was asleep for during
    a shift.
    """
    for prev_event, next_event in zipper(shift):
        if prev_event['event'] == 'falls asleep':
            assert next_event['event'] == 'wakes up'  # assumption about input
            start = prev_event['timestamp']
            end = next_event['timestamp'] - dt.timedelta(minutes=1)
            yield start, end


def part1():
    events = read_input()
    shifts = get_shifts(events)

    # For each guard, the total amount of time they slept
    total_time_slept = {guard: sum(map(time_asleep, guard_shifts))
                        for guard, guard_shifts in shifts.items()}

    # The guard that slept the most, and the corresponding amount of time
    guard_most_asleep, most_time_slept = max(total_time_slept.items(), key=itemgetter(1))

    # For the guard that slept the most, a count of the minute numbers they were asleep
    minute_numbers_asleep = Counter()
    for shift in shifts[guard_most_asleep]:
        for sleep_interval in intervals_asleep(shift):
            for d in range_minute(*sleep_interval):
                minute_numbers_asleep[d.minute] += 1

    # For the guard that slept the most, the minute number they were most frequently asleep
    minute_most_slept, _ = max(minute_numbers_asleep.items(), key=itemgetter(1))

    answer = guard_most_asleep * minute_most_slept
    return answer


def part2():
    events = read_input()
    shifts = get_shifts(events)

    # For each guard, a count of the minute numbers they were asleep
    guard_minute_numbers_asleep = defaultdict(Counter)
    for guard, guard_shifts in shifts.items():
        for shift in guard_shifts:
            for sleep_interval in intervals_asleep(shift):
                for d in range_minute(*sleep_interval):
                    guard_minute_numbers_asleep[guard][d.minute] += 1

    # For each guard, the minute number they were most frequently asleep
    guard_minute_most_asleep = dict()
    for guard, minute_count in guard_minute_numbers_asleep.items():
        minute, frequency = max(minute_count.items(), key=itemgetter(1))
        guard_minute_most_asleep[guard] = {'minute': minute, 'frequency': frequency}

    # The guard that was most frequently asleep on the same minute, and the
    # corresponding minute and frequency.
    guard, minute_freq = max(guard_minute_most_asleep.items(),
                             key=lambda x: x[1]['frequency'])

    answer = guard * minute_freq['minute']
    return answer


print('Part 1:', part1())
print('Part 2:', part2())
