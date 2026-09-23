import random

from src.config import GAConfig
from src.crossover import order_crossover
from src.fitness import tour_distance
from src.mutation import swap_mutation
from src.selection import tournament_selection
from src.tsp import City


def create_next_generation(
    population: list[list[int]],
    cities: list[City],
    config: GAConfig,
    rng: random.Random,
) -> list[list[int]]:
    """
    Create one new generation using:

    - elitism
    - tournament selection
    - order crossover
    - swap mutation
    """

    if len(population) != config.population_size:
        raise ValueError(
            "Population size does not match configuration."
        )

    if config.elitism < 0:
        raise ValueError("Elitism cannot be negative.")

    if config.elitism > len(population):
        raise ValueError(
            "Elitism cannot exceed population size."
        )

    # Sort population from best to worst.
    sorted_population = sorted(
        population,
        key=lambda individual: tour_distance(
            individual,
            cities,
        ),
    )

    # Preserve the best individuals.
    next_population = [
        individual.copy()
        for individual in sorted_population[:config.elitism]
    ]

    # Generate children until the new population is full.
    while len(next_population) < config.population_size:

        parent_1 = tournament_selection(
            population=population,
            cities=cities,
            tournament_size=config.tournament_size,
            rng=rng,
        )

        parent_2 = tournament_selection(
            population=population,
            cities=cities,
            tournament_size=config.tournament_size,
            rng=rng,
        )

        # Crossover
        if rng.random() < config.crossover_rate:
            child_1, child_2 = order_crossover(
                parent_1,
                parent_2,
                rng,
            )
        else:
            child_1 = parent_1.copy()
            child_2 = parent_2.copy()

        # Mutation
        if rng.random() < config.mutation_rate:
            child_1 = swap_mutation(
                child_1,
                rng,
            )

        if rng.random() < config.mutation_rate:
            child_2 = swap_mutation(
                child_2,
                rng,
            )

        next_population.append(child_1)

        # Important when population size is odd.
        if len(next_population) < config.population_size:
            next_population.append(child_2)

    return next_population