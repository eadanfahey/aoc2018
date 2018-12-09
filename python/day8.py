from os.path import join, dirname, pardir


INPUT = join(dirname(__file__), pardir, 'input/day8.txt')


def read_input():
    with open(INPUT) as f:
        return [int(i) for i in f.read().split()]


def parse_tree(remaining):
    """Recursively parse the input to form the tree."""
    num_children, num_metadata = remaining[:2]
    remaining = remaining[2:]

    children = []
    for _ in range(num_children):
        child, remaining = parse_tree(remaining)
        children.append(child)

    node = {'children': children, 'metadata': remaining[:num_metadata]}
    return node, remaining[num_metadata:]


def sum_metadata(tree):
    return sum(tree['metadata']) + sum(sum_metadata(c) for c in tree['children'])


def value(node):
    children, metadata = node['children'], node['metadata']
    if not children:
        return sum(metadata)
    else:
        return sum(value(children[i-1]) for i in metadata if i - 1 < len(children))


def part1():
    numbers = read_input()
    tree, _ = parse_tree(numbers)
    return sum_metadata(tree)


def part2():
    numbers = read_input()
    tree, _ = parse_tree(numbers)
    return value(tree)


print('Part 1:', part1())
print('Part 2:', part2())
