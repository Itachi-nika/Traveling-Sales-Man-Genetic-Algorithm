import random


""" Step 1: Select two different positions in the route at random

    Step 2: Swap the cities located at the selected positions

    Step 3: Keep all other cities unchanged

    Step 4: Return the mutated route as a valid TSP individual  """

def swap_mutation(
    individual: list[int],
    rng: random.Random,
) -> list[int]:
 

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