from dataclasses import dataclass, replace

from src.config import GAConfig
from src.genetic_algorithm import (
    GAResult,
    run_genetic_algorithm,
)
from src.tsp import generate_cities
import statistics


@dataclass(frozen=True)
class ExperimentRun:
    experiment_name: str
    parameter_name: str
    parameter_value: int | float

    problem_seed: int
    ga_seed: int

    config: GAConfig
    result: GAResult


def run_experiment_once(
    experiment_name: str,
    parameter_name: str,
    config: GAConfig,
    problem_seed: int,
    ga_seed: int,
) -> ExperimentRun:
    """
    Run one experimental GA trial and attach
    all metadata required to reproduce it.
    """

    if not experiment_name:
        raise ValueError(
            "Experiment name cannot be empty."
        )

    if not hasattr(config, parameter_name):
        raise ValueError(
            f"Unknown configuration parameter: "
            f"{parameter_name}"
        )

    parameter_value = getattr(
        config,
        parameter_name,
    )

    if not isinstance(parameter_value, (int, float)):
        raise ValueError(
            "Experimental parameter must be numeric."
        )

    cities = generate_cities(
        num_cities=config.num_cities,
        seed=problem_seed,
    )

    result = run_genetic_algorithm(
        cities=cities,
        config=config,
        seed=ga_seed,
    )

    return ExperimentRun(
        experiment_name=experiment_name,
        parameter_name=parameter_name,
        parameter_value=parameter_value,
        problem_seed=problem_seed,
        ga_seed=ga_seed,
        config=config,
        result=result,
    )

def run_experiment_repeated(
    experiment_name: str,
    parameter_name: str,
    config: GAConfig,
    problem_seed: int,
    ga_seeds: list[int],
) -> list[ExperimentRun]:
    """
    Run the same experimental configuration
    multiple times using different GA seeds.
    """

    if not ga_seeds:
        raise ValueError(
            "At least one GA seed is required."
        )

    if len(set(ga_seeds)) != len(ga_seeds):
        raise ValueError(
            "GA seeds must be unique."
        )

    return [
        run_experiment_once(
            experiment_name=experiment_name,
            parameter_name=parameter_name,
            config=config,
            problem_seed=problem_seed,
            ga_seed=ga_seed,
        )
        for ga_seed in ga_seeds
    ]

@dataclass(frozen=True)
class ExperimentSummary:
    experiment_name: str
    parameter_name: str
    parameter_value: int | float

    num_runs: int

    mean_best_distance: float
    median_best_distance: float
    std_best_distance: float
    min_best_distance: float
    max_best_distance: float

    mean_runtime_seconds: float
    std_runtime_seconds: float

def summarize_experiment_runs(
    runs: list[ExperimentRun],
) -> ExperimentSummary:
    """
    Summarize repeated runs for one experimental
    parameter configuration.
    """

    if not runs:
        raise ValueError(
            "At least one experiment run is required."
        )

    first = runs[0]

    for run in runs[1:]:
        if run.experiment_name != first.experiment_name:
            raise ValueError(
                "All runs must belong to the same experiment."
            )

        if run.parameter_name != first.parameter_name:
            raise ValueError(
                "All runs must vary the same parameter."
            )

        if run.parameter_value != first.parameter_value:
            raise ValueError(
                "All runs must use the same parameter value."
            )

        if run.problem_seed != first.problem_seed:
            raise ValueError(
                "All runs must use the same problem seed."
            )

        if run.config != first.config:
            raise ValueError(
                "All runs must use the same configuration."
            )

    best_distances = [
        run.result.best_distance
        for run in runs
    ]

    runtimes = [
        run.result.runtime_seconds
        for run in runs
    ]

    # Standard deviation is undefined for a single
    # observation, so use 0.0 for a one-run summary.
    if len(runs) > 1:
        std_best_distance = statistics.stdev(
            best_distances
        )

        std_runtime_seconds = statistics.stdev(
            runtimes
        )
    else:
        std_best_distance = 0.0
        std_runtime_seconds = 0.0

    return ExperimentSummary(
        experiment_name=first.experiment_name,
        parameter_name=first.parameter_name,
        parameter_value=first.parameter_value,
        num_runs=len(runs),

        mean_best_distance=statistics.mean(
            best_distances
        ),

        median_best_distance=statistics.median(
            best_distances
        ),

        std_best_distance=std_best_distance,

        min_best_distance=min(
            best_distances
        ),

        max_best_distance=max(
            best_distances
        ),

        mean_runtime_seconds=statistics.mean(
            runtimes
        ),

        std_runtime_seconds=std_runtime_seconds,
    )

@dataclass(frozen=True)
class ParameterSweepResult:
    runs: list[ExperimentRun]
    summaries: list[ExperimentSummary]

def run_parameter_sweep(
    experiment_name: str,
    parameter_name: str,
    values: list[int | float],
    baseline: GAConfig,
    problem_seed: int,
    ga_seeds: list[int],
) -> ParameterSweepResult:
    """
    Run an experiment for multiple values of one
    configuration parameter.

    All parameters except parameter_name remain
    fixed at their baseline values.
    """

    if not values:
        raise ValueError(
            "At least one parameter value is required."
        )

    if len(set(values)) != len(values):
        raise ValueError(
            "Parameter values must be unique."
        )

    if not hasattr(baseline, parameter_name):
        raise ValueError(
            f"Unknown configuration parameter: "
            f"{parameter_name}"
        )

    all_runs = []
    summaries = []

    for value in values:
        if not isinstance(value, (int, float)):
            raise ValueError(
                "Parameter values must be numeric."
            )

        config = replace(
            baseline,
            **{parameter_name: value},
        )

        runs = run_experiment_repeated(
            experiment_name=experiment_name,
            parameter_name=parameter_name,
            config=config,
            problem_seed=problem_seed,
            ga_seeds=ga_seeds,
        )

        summary = summarize_experiment_runs(
            runs
        )

        all_runs.extend(runs)
        summaries.append(summary)

    return ParameterSweepResult(
        runs=all_runs,
        summaries=summaries,
    )