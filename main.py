from src.config import BASELINE
from src.genetic_algorithm import run_genetic_algorithm
from src.tsp import generate_cities

#Just a test to make sure everything is working and the genetic algorithm runs with the baseline configuration
#Our main is in experiments/..., this is just a test to make sure everything is working and the genetic algorithm runs with the baseline configuration
#before we run the bigger experiments.
#Ignore this..

# FILIP YOUSIF : experiments/experiment_a_cities.py is the main experiment file for Experiment A
# JOHN MOLIN  : experiments/experiment_b/run.py is the main experiment file for Experiment B
# SAMUEL YOUSEF : experiments/experiment_c_population.py is the main experiment file for Experiment C
# MAJD MORAD : experiments/experiment_d_mutation.py is the main experiment file for Experiment D

def main():
    problem_seed = 12345
    ga_seed = 42

    cities = generate_cities(
        num_cities=BASELINE.num_cities,
        seed=problem_seed,
    )

    result = run_genetic_algorithm(
        cities=cities,
        config=BASELINE,
        seed=ga_seed,
    )

    print("Baseline GA run")
    print("----------------")
    print(f"Cities: {BASELINE.num_cities}")
    print(f"Population size: {BASELINE.population_size}")
    print(f"Generations: {BASELINE.generations}")
    print(f"Mutation rate: {BASELINE.mutation_rate}")
    print(f"Crossover rate: {BASELINE.crossover_rate}")
    print()

    print(
        f"Initial best distance: "
        f"{result.history[0].best_distance:.2f}"
    )

    print(
        f"Final generation best distance: "
        f"{result.history[-1].best_distance:.2f}"
    )

    print(
        f"Best distance found: "
        f"{result.best_distance:.2f}"
    )

    print()
    print("Best route:")
    print(result.best_route)
    print("\nProgress:")
    print("Generation | Best distance | Mean distance")
    print("-------------------------------------------")

    for stats in result.history:
        if stats.generation % 50 == 0:
            print(
                f"{stats.generation:10d} | "
                f"{stats.best_distance:13.2f} | "
                f"{stats.mean_distance:13.2f}"
            )
    print()
    print("Measurements:")
    print(
        f"Initial best distance: "
        f"{result.initial_best_distance:.2f}"
    )
    print(
        f"Best distance: "
        f"{result.best_distance:.2f}"
    )
    print(
        f"Runtime: "
        f"{result.runtime_seconds:.4f} seconds"
    )
    print(
        f"Population evaluations: "
        f"{result.population_evaluations}"
    )



if __name__ == "__main__":
    main()