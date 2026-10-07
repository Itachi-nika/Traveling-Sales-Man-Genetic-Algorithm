import random

from src.fitness import tour_distance
from src.tsp import City

""" Step 1: Randomly select a number of individuals from the population

    Step 2: Evaluate the selected individuals using their total tour distance

    Step 3: Compare the selected individuals

    Step 4: Choose the individual with the shortest tour distance as the winner

    Step 5: Return the winner as a parent for reproduction      """


def tournament_selection(
    population: list[list[int]],
    cities: list[City],
    tournament_size: int,
    rng: random.Random,
) -> list[int]:
    
#ErrorChecking
    if tournament_size < 1:
        raise ValueError("Tournament size must be at least 1.")

    if tournament_size > len(population):
        raise ValueError(
            "Tournament size cannot exceed population size."
        )

    competitors = rng.sample(
        population,
        tournament_size,
    )

    winner = min(
        competitors,
        key=lambda individual: tour_distance(
            individual,
            cities,
        ),
    )

    return winner.copy()