import math

from src.tsp import City

"""
    Step 1: Start with a total tour distance of zero

    Step 2: Calculate the Euclidean distance between each city and the next city in the route

    Step 3: Add each distance to the total tour distance

    Step 4: Include the distance from the final city back to the first city

    Step 5: Use the total tour distance as the evaluation value, where a shorter distance represents a better individual    """


def euclidean_distance(city_a: City, city_b: City) -> float:
    return math.hypot(
        city_a.x - city_b.x,
        city_a.y - city_b.y,
    )

def tour_distance(
    route: list[int],
    cities: list[City],
) -> float:

    if len(route) != len(cities):
        raise ValueError(
            "Route must contain exactly one entry for every city."
        )

    if set(route) != set(range(len(cities))):
        raise ValueError(
            "Route must be a permutation of all city indices."
        )

    total_distance = 0.0

    for i in range(len(route)):
        current_city = cities[route[i]]
        next_city = cities[route[(i + 1) % len(route)]]

        total_distance += euclidean_distance(
            current_city,
            next_city,
        )

    return total_distance