import random


def swap_mutation(
    individual: list[int],
    rng: random.Random,
) -> list[int]:
    """
    Perform swap mutation on a TSP individual.

    Two different positions are selected randomly
    and their cities are swapped.

    The original individual is not modified.
    """

    if len(individual) < 2:
        raise ValueError(
            "Individual must contain at least two cities."
        )

    mutated = individual.copy()

    index_1, index_2 = rng.sample(
        range(len(mutated)),
        2,
    )

    mutated[index_1], mutated[index_2] = (
        mutated[index_2],
        mutated[index_1],
    )

    return mutated