from dataclasses import dataclass
import random
import time

from src.config import GAConfig
from src.evolution import create_next_generation
from src.fitness import tour_distance
from src.metrics import (
    GenerationStats,
    calculate_generation_stats,
)
from src.population import create_population
from src.tsp import City


""" Step 1: Generate the initial population of valid routes

    Step 2: Evaluate the initial population and store the best route found

    Step 3: For each generation:
        Create the next generation using elitism, tournament selection, crossover, and mutation
        Evaluate the new population
        Compare the best individual in the current generation with the best route found so far
        Update the best route if a better solution is found
        Store the generation statistics

    Step 4: Continue until the specified number of generations has been completed

    Step 5: Calculate the total runtime and number of population evaluations

    Step 6: Return the best route, best distance, initial best distance, generation history, runtime, and evaluation count  """

#Custom Class to hold the results of the genetic algorithm run
@dataclass
class GAResult:
    best_route: list[int]
    best_distance: float
    initial_best_distance: float
    history: list[GenerationStats]
    runtime_seconds: float
    population_evaluations: int

#Main function to run the genetic algorithm
def run_genetic_algorithm(
    cities: list[City],
    config: GAConfig,
    seed: int,
) -> GAResult:
    
#ErrorChecking to make sure the configuration and inputs are valid
    if len(cities) != config.num_cities:
        raise ValueError(
            "Number of cities does not match configuration."
        )

    if config.generations < 0:
        raise ValueError(
            "Number of generations cannot be negative."
        )
#Measure the start time of the algorithm to calculate runtime 
    start_time = time.perf_counter()

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

    initial_best_distance = history[0].best_distance

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

    runtime_seconds = time.perf_counter() - start_time

    population_evaluations = (
        config.population_size
        * (config.generations + 1)
    )

    return GAResult(
        best_route=best_route,
        best_distance=best_distance,
        initial_best_distance=initial_best_distance,
        history=history,
        runtime_seconds=runtime_seconds,
        population_evaluations=population_evaluations,
    )