import random

from src.config import GAConfig
from src.evolution import create_next_generation
from src.population import create_population
from src.tsp import generate_cities
from src.tsp import City


def test_next_generation_has_correct_size():
    config = GAConfig(
        num_cities=10,
        population_size=20,
        generations=100,
        crossover_rate=0.9,
        mutation_rate=0.05,
        tournament_size=3,
        elitism=2,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    rng = random.Random(42)

    population = create_population(
        num_cities=config.num_cities,
        population_size=config.population_size,
        rng=rng,
    )

    next_population = create_next_generation(
        population=population,
        cities=cities,
        config=config,
        rng=rng,
    )

    assert len(next_population) == config.population_size


def test_next_generation_contains_valid_individuals():
    config = GAConfig(
        num_cities=10,
        population_size=20,
        generations=100,
        crossover_rate=0.9,
        mutation_rate=0.2,
        tournament_size=3,
        elitism=2,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    rng = random.Random(42)

    population = create_population(
        num_cities=config.num_cities,
        population_size=config.population_size,
        rng=rng,
    )

    next_population = create_next_generation(
        population,
        cities,
        config,
        rng,
    )

    expected = list(range(config.num_cities))

    for individual in next_population:
        assert sorted(individual) == expected


from src.fitness import tour_distance


def test_elite_individual_is_preserved():
    config = GAConfig(
        num_cities=4,
        population_size=3,
        generations=10,
        crossover_rate=0.9,
        mutation_rate=0.1,
        tournament_size=2,
        elitism=1,
    )

    cities = [
        # Square
        # Best route below has distance 4
        City(0, 0),
        City(1, 0),
        City(1, 1),
        City(0, 1),
    ]

    best = [0, 1, 2, 3]

    population = [
        best,
        [0, 2, 1, 3],
        [0, 1, 3, 2],
    ]

    rng = random.Random(42)

    next_population = create_next_generation(
        population,
        cities,
        config,
        rng,
    )

    assert best in next_population


def test_same_seed_produces_same_generation():
    config = GAConfig(
        num_cities=10,
        population_size=20,
        generations=100,
        crossover_rate=0.9,
        mutation_rate=0.1,
        tournament_size=3,
        elitism=2,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    population_rng = random.Random(999)

    population = create_population(
        num_cities=config.num_cities,
        population_size=config.population_size,
        rng=population_rng,
    )

    rng_1 = random.Random(42)
    rng_2 = random.Random(42)

    generation_1 = create_next_generation(
        population,
        cities,
        config,
        rng_1,
    )

    generation_2 = create_next_generation(
        population,
        cities,
        config,
        rng_2,
    )

    assert generation_1 == generation_2

def test_odd_population_size_is_preserved():
    config = GAConfig(
        num_cities=10,
        population_size=11,
        generations=100,
        crossover_rate=0.9,
        mutation_rate=0.1,
        tournament_size=3,
        elitism=2,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    rng = random.Random(42)

    population = create_population(
        num_cities=config.num_cities,
        population_size=config.population_size,
        rng=rng,
    )

    next_population = create_next_generation(
        population,
        cities,
        config,
        rng,
    )

    assert len(next_population) == 11

def test_next_generation_does_not_modify_original_population():
    config = GAConfig(
        num_cities=10,
        population_size=20,
        generations=100,
        crossover_rate=0.9,
        mutation_rate=0.1,
        tournament_size=3,
        elitism=2,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    population_rng = random.Random(999)

    population = create_population(
        num_cities=config.num_cities,
        population_size=config.population_size,
        rng=population_rng,
    )

    original_population = [
        individual.copy()
        for individual in population
    ]

    rng = random.Random(42)

    create_next_generation(
        population=population,
        cities=cities,
        config=config,
        rng=rng,
    )

    assert population == original_population