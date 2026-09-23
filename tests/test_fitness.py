import pytest

from src.tsp import City
from src.fitness import tour_distance


def test_square_tour_distance():

    cities = [
        City(0, 0),
        City(1, 0),
        City(1, 1),
        City(0, 1),
    ]

    route = [0, 1, 2, 3]

    distance = tour_distance(route, cities)

    assert distance == pytest.approx(4.0)