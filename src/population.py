import random


"""
    Step 1: Create a route containing every city exactly once

    Step 2: Randomly shuffle the order of the cities to form a valid TSP individual

    Step 3: Repeat the process until the required population size is reached

    Step 4: Store all generated individuals as the initial population

    Step 5: Return the complete population  """


def create_individual(
    num_cities: int,
    rng: random.Random,
) -> list[int]:
    
    #Create one valid TSP individual.

    #An individual is represented as a permutation
    #of city indices: [0, 1, ..., num_cities - 1].
    
    #ErrorChecking
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
   
#   Create the initial population of TSP individuals.
    if population_size < 1:
        raise ValueError("Population size must be at least 1.")

    return [
        create_individual(num_cities, rng)
        for _ in range(population_size)
    ]