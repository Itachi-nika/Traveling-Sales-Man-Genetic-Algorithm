from dataclasses import dataclass


@dataclass(frozen=True)
class GAConfig:
    num_cities: int = 50
    population_size: int = 200
    generations: int = 500

    crossover_rate: float = 0.90
    mutation_rate: float = 0.05

    tournament_size: int = 3
    elitism: int = 2


BASELINE = GAConfig()