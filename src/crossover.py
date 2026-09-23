import random


def order_crossover(
    parent_1: list[int],
    parent_2: list[int],
    rng: random.Random,
) -> tuple[list[int], list[int]]:
    """
    Perform Order Crossover (OX) on two TSP parents.

    Returns two children that are valid permutations.
    """

    if len(parent_1) != len(parent_2):
        raise ValueError("Parents must have the same length.")

    if len(parent_1) < 2:
        raise ValueError("Parents must contain at least two cities.")

    if set(parent_1) != set(parent_2):
        raise ValueError(
            "Parents must contain the same cities."
        )

    size = len(parent_1)

    start, end = sorted(
        rng.sample(range(size), 2)
    )

    child_1 = _create_child(
        parent_1,
        parent_2,
        start,
        end,
    )

    child_2 = _create_child(
        parent_2,
        parent_1,
        start,
        end,
    )

    return child_1, child_2


def _create_child(
    segment_parent: list[int],
    fill_parent: list[int],
    start: int,
    end: int,
) -> list[int]:
    """
    Create one child using Order Crossover.
    """

    size = len(segment_parent)

    child = [None] * size

    # Copy a segment from the first parent.
    child[start:end + 1] = segment_parent[start:end + 1]

    # Read cities from the second parent starting
    # immediately after the crossover segment.
    fill_values = []

    for offset in range(size):
        index = (end + 1 + offset) % size
        city = fill_parent[index]

        if city not in child:
            fill_values.append(city)

    # Fill empty positions starting immediately
    # after the copied segment.
    fill_index = 0

    for offset in range(size):
        index = (end + 1 + offset) % size

        if child[index] is None:
            child[index] = fill_values[fill_index]
            fill_index += 1

    return child