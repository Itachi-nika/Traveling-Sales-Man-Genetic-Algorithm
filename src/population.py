import random


def create_individual(
    num_cities: int,
    rng: random.Random,
) -> list[int]:
    """
    Create one valid TSP individual.

    An individual is represented as a permutation
    of city indices: [0, 1, ..., num_cities - 1].
    """

    if num_cities < 2:
        raise ValueError("TSP requires at least two cities.")

    route = list(range(num_cities))
    rng.shuffle(route)

    return route


def create_population(
    num_cities: int,
    population_size: int,
    rng: random.Random,
) -> list[list[int]]:
    """
    Create a population of valid TSP individuals.
    """

    if population_size < 1:
        raise ValueError("Population size must be at least 1.")

    return [
        create_individual(num_cities, rng)
        for _ in range(population_size)
    ]