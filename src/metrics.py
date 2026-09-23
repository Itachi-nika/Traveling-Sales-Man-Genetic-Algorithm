from dataclasses import dataclass

from src.fitness import tour_distance
from src.tsp import City


@dataclass(frozen=True)
class GenerationStats:
    generation: int
    best_distance: float
    mean_distance: float


def calculate_generation_stats(
    population: list[list[int]],
    cities: list[City],
    generation: int,
) -> GenerationStats:
    """
    Calculate summary statistics for one generation.
    """

    if not population:
        raise ValueError("Population cannot be empty.")

    distances = [
        tour_distance(individual, cities)
        for individual in population
    ]

    return GenerationStats(
        generation=generation,
        best_distance=min(distances),
        mean_distance=sum(distances) / len(distances),
    )