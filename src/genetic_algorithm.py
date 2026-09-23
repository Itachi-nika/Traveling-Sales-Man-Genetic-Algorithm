from dataclasses import dataclass
import random

from src.config import GAConfig
from src.evolution import create_next_generation
from src.fitness import tour_distance
from src.metrics import (
    GenerationStats,
    calculate_generation_stats,
)
from src.population import create_population
from src.tsp import City


@dataclass
class GAResult:
    best_route: list[int]
    best_distance: float
    history: list[GenerationStats]


def run_genetic_algorithm(
    cities: list[City],
    config: GAConfig,
    seed: int,
) -> GAResult:
    """
    Run the complete genetic algorithm.

    Returns the best solution observed during the run
    together with statistics for every generation.
    """

    if len(cities) != config.num_cities:
        raise ValueError(
            "Number of cities does not match configuration."
        )

    if config.generations < 0:
        raise ValueError(
            "Number of generations cannot be negative."
        )

    rng = random.Random(seed)

    population = create_population(
        num_cities=config.num_cities,
        population_size=config.population_size,
        rng=rng,
    )

    history = [
        calculate_generation_stats(
            population=population,
            cities=cities,
            generation=0,
        )
    ]

    best_route = min(
        population,
        key=lambda individual: tour_distance(
            individual,
            cities,
        ),
    ).copy()

    best_distance = tour_distance(
        best_route,
        cities,
    )

    for generation in range(
        1,
        config.generations + 1,
    ):
        population = create_next_generation(
            population=population,
            cities=cities,
            config=config,
            rng=rng,
        )

        stats = calculate_generation_stats(
            population=population,
            cities=cities,
            generation=generation,
        )

        history.append(stats)

        generation_best = min(
            population,
            key=lambda individual: tour_distance(
                individual,
                cities,
            ),
        )

        generation_best_distance = tour_distance(
            generation_best,
            cities,
        )

        if generation_best_distance < best_distance:
            best_distance = generation_best_distance
            best_route = generation_best.copy()

    return GAResult(
        best_route=best_route,
        best_distance=best_distance,
        history=history,
    )