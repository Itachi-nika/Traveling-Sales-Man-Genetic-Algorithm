import random

""" Step 1: Randomly select two crossover positions

    Step 2: Copy the segment between the crossover positions from each parent into the corresponding child

    Step 3: Starting after the copied segment, read the cities from the other parent in circular order

    Step 4: Skip cities that are already present in the child

    Step 5: Fill the remaining empty positions with the unused cities in the order they are encountered

    Step 6: Repeat the same process in the opposite direction to create the second child

    Step 7: Return both valid offspring     """


def order_crossover(
    parent_1: list[int],
    parent_2: list[int],
    rng: random.Random,
) -> tuple[list[int], list[int]]:
    #Check that parents are valid
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
  
    size = len(segment_parent)

    child = [None] * size

    
    child[start:end + 1] = segment_parent[start:end + 1]

   
    fill_values = []

    for offset in range(size):
        index = (end + 1 + offset) % size
        city = fill_parent[index]

        if city not in child:
            fill_values.append(city)

   
    fill_index = 0

    for offset in range(size):
        index = (end + 1 + offset) % size

        if child[index] is None:
            child[index] = fill_values[fill_index]
            fill_index += 1

    return child