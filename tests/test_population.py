import random

import pytest

from src.population import (
    create_individual,
    create_population,
)


def test_individual_contains_all_cities():
    rng = random.Random(42)

    individual = create_individual(
        num_cities=10,
        rng=rng,
    )

    assert sorted(individual) == list(range(10))


def test_individual_has_correct_length():
    rng = random.Random(42)

    individual = create_individual(
        num_cities=10,
        rng=rng,
    )

    assert len(individual) == 10


def test_population_has_correct_size():
    rng = random.Random(42)

    population = create_population(
        num_cities=10,
        population_size=50,
        rng=rng,
    )

    assert len(population) == 50


def test_every_individual_is_valid():
    rng = random.Random(42)

    population = create_population(
        num_cities=10,
        population_size=50,
        rng=rng,
    )

    expected_cities = list(range(10))

    for individual in population:
        assert sorted(individual) == expected_cities


def test_same_seed_produces_same_population():
    rng_1 = random.Random(42)
    rng_2 = random.Random(42)

    population_1 = create_population(
        num_cities=10,
        population_size=20,
        rng=rng_1,
    )

    population_2 = create_population(
        num_cities=10,
        population_size=20,
        rng=rng_2,
    )

    assert population_1 == population_2


def test_invalid_population_size():
    rng = random.Random(42)

    with pytest.raises(ValueError):
        create_population(
            num_cities=10,
            population_size=0,
            rng=rng,
        )