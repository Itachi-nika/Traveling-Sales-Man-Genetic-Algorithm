import pytest

from src.metrics import calculate_generation_stats
from src.tsp import City


def test_generation_statistics():
    cities = [
        City(0, 0),
        City(1, 0),
        City(1, 1),
        City(0, 1),
    ]

    population = [
        [0, 1, 2, 3],
        [0, 2, 1, 3],
    ]

    stats = calculate_generation_stats(
        population=population,
        cities=cities,
        generation=5,
    )

    assert stats.generation == 5
    assert stats.best_distance == pytest.approx(4.0)
    assert stats.mean_distance >= stats.best_distance


def test_empty_population_raises_error():
    cities = [
        City(0, 0),
        City(1, 0),
    ]

    with pytest.raises(ValueError):
        calculate_generation_stats(
            population=[],
            cities=cities,
            generation=0,
        )