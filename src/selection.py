import random

from src.fitness import tour_distance
from src.tsp import City


def tournament_selection(
    population: list[list[int]],
    cities: list[City],
    tournament_size: int,
    rng: random.Random,
) -> list[int]:
    """
    Select one parent using tournament selection.

    A number of individuals are sampled randomly from the population.
    The individual with the shortest tour distance wins.
    """

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