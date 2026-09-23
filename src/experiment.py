from dataclasses import dataclass

from src.config import GAConfig
from src.genetic_algorithm import GAResult


@dataclass(frozen=True)
class ExperimentRun:
    experiment_name: str
    parameter_name: str
    parameter_value: int | float

    problem_seed: int
    ga_seed: int

    config: GAConfig
    result: GAResult