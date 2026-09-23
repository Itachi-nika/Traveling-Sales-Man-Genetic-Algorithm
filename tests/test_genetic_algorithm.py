from dataclasses import replace

import pytest

from src.config import BASELINE
from src.fitness import tour_distance
from src.genetic_algorithm import run_genetic_algorithm
from src.tsp import generate_cities


def test_history_has_correct_length():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=10,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    result = run_genetic_algorithm(
        cities=cities,
        config=config,
        seed=42,
    )

    assert len(result.history) == 11


def test_history_generation_numbers():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    result = run_genetic_algorithm(
        cities,
        config,
        seed=42,
    )

    generations = [
        stats.generation
        for stats in result.history
    ]

    assert generations == [0, 1, 2, 3, 4, 5]


def test_best_distance_matches_best_route():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=10,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    result = run_genetic_algorithm(
        cities,
        config,
        seed=42,
    )

    actual_distance = tour_distance(
        result.best_route,
        cities,
    )

    assert result.best_distance == pytest.approx(
        actual_distance
    )

def test_best_result_is_not_worse_than_initial_best():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=20,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    result = run_genetic_algorithm(
        cities,
        config,
        seed=42,
    )

    initial_best = result.history[0].best_distance

    assert result.best_distance <= initial_best


def test_same_seed_produces_same_result():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=10,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    result_1 = run_genetic_algorithm(
        cities,
        config,
        seed=42,
    )

    result_2 = run_genetic_algorithm(
        cities,
        config,
        seed=42,
    )

    assert result_1.best_route == result_2.best_route

    assert result_1.best_distance == pytest.approx(
        result_2.best_distance
    )

    assert result_1.initial_best_distance == pytest.approx(
        result_2.initial_best_distance
    )

    assert result_1.history == result_2.history

    assert (
        result_1.population_evaluations
        == result_2.population_evaluations
    )


def test_best_distance_never_increases_with_elitism():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=20,
        elitism=1,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    result = run_genetic_algorithm(
        cities=cities,
        config=config,
        seed=42,
    )

    best_distances = [
        stats.best_distance
        for stats in result.history
    ]

    for previous, current in zip(
        best_distances,
        best_distances[1:],
    ):
        assert current <= previous


def test_initial_best_distance_matches_history():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    result = run_genetic_algorithm(
        cities=cities,
        config=config,
        seed=42,
    )

    assert result.initial_best_distance == pytest.approx(
        result.history[0].best_distance
    )

def test_runtime_is_non_negative():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    result = run_genetic_algorithm(
        cities=cities,
        config=config,
        seed=42,
    )

    assert result.runtime_seconds >= 0.0

def test_population_evaluations_are_correct():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=123,
    )

    result = run_genetic_algorithm(
        cities=cities,
        config=config,
        seed=42,
    )

    assert result.population_evaluations == 20 * 6

