from dataclasses import dataclass
import random


@dataclass(frozen=True)
class City:
    x: float
    y: float


def generate_cities(
    num_cities: int,
    seed: int,
    min_coordinate: float = 0.0,
    max_coordinate: float = 100.0,
) -> list[City]:

    if num_cities < 2:
        raise ValueError("TSP requires at least two cities.")

    rng = random.Random(seed)

    return [
        City(
            x=rng.uniform(min_coordinate, max_coordinate),
            y=rng.uniform(min_coordinate, max_coordinate),
        )
        for _ in range(num_cities)
    ]