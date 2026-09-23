import random

import pytest

from src.selection import tournament_selection
from src.tsp import City


def test_tournament_selects_best_individual():
    cities = [
        City(0, 0),
        City(1, 0),
        City(1, 1),
        City(0, 1),
    ]

    good_route = [0, 1, 2, 3]
    worse_route = [0, 2, 1, 3]

    population = [
        good_route,
        worse_route,
    ]

    rng = random.Random(42)

    selected = tournament_selection(
        population=population,
        cities=cities,
        tournament_size=2,
        rng=rng,
    )

    assert selected == good_route


def test_tournament_returns_valid_individual():
    cities = [
        City(0, 0),
        City(1, 0),
        City(1, 1),
        City(0, 1),
    ]

    population = [
        [0, 1, 2, 3],
        [0, 2, 1, 3],
        [3, 2, 1, 0],
    ]

    rng = random.Random(42)

    selected = tournament_selection(
        population=population,
        cities=cities,
        tournament_size=2,
        rng=rng,
    )

    assert sorted(selected) == [0, 1, 2, 3]


def test_selection_returns_copy():
    cities = [
        City(0, 0),
        City(1, 0),
        City(1, 1),
        City(0, 1),
    ]

    population = [
        [0, 1, 2, 3],
    ]

    rng = random.Random(42)

    selected = tournament_selection(
        population=population,
        cities=cities,
        tournament_size=1,
        rng=rng,
    )

    assert selected == population[0]
    assert selected is not population[0]


def test_invalid_tournament_size_zero():
    cities = [
        City(0, 0),
        City(1, 0),
    ]

    population = [
        [0, 1],
    ]

    rng = random.Random(42)

    with pytest.raises(ValueError):
        tournament_selection(
            population=population,
            cities=cities,
            tournament_size=0,
            rng=rng,
        )


def test_tournament_size_larger_than_population():
    cities = [
        City(0, 0),
        City(1, 0),
    ]

    population = [
        [0, 1],
    ]

    rng = random.Random(42)

    with pytest.raises(ValueError):
        tournament_selection(
            population=population,
            cities=cities,
            tournament_size=2,
            rng=rng,
        )