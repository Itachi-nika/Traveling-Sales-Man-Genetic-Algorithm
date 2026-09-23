import csv
from pathlib import Path

from src.experiment import ExperimentRun


def export_runs_csv(
    runs: list[ExperimentRun],
    file_path: str | Path,
) -> None:
    """
    Export one row per experimental GA run.
    """

    if not runs:
        raise ValueError(
            "At least one experiment run is required."
        )

    path = Path(file_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "experiment_name",
        "parameter_name",
        "parameter_value",
        "problem_seed",
        "ga_seed",
        "num_cities",
        "population_size",
        "generations",
        "crossover_rate",
        "mutation_rate",
        "tournament_size",
        "elitism",
        "initial_best_distance",
        "best_distance",
        "runtime_seconds",
        "population_evaluations",
    ]

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for run in runs:
            writer.writerow({
                "experiment_name":
                    run.experiment_name,

                "parameter_name":
                    run.parameter_name,

                "parameter_value":
                    run.parameter_value,

                "problem_seed":
                    run.problem_seed,

                "ga_seed":
                    run.ga_seed,

                "num_cities":
                    run.config.num_cities,

                "population_size":
                    run.config.population_size,

                "generations":
                    run.config.generations,

                "crossover_rate":
                    run.config.crossover_rate,

                "mutation_rate":
                    run.config.mutation_rate,

                "tournament_size":
                    run.config.tournament_size,

                "elitism":
                    run.config.elitism,

                "initial_best_distance":
                    run.result.initial_best_distance,

                "best_distance":
                    run.result.best_distance,

                "runtime_seconds":
                    run.result.runtime_seconds,

                "population_evaluations":
                    run.result.population_evaluations,
            })


def export_history_csv(
    runs: list[ExperimentRun],
    file_path: str | Path,
) -> None:
    """
    Export generation-by-generation history
    for all provided experiment runs.
    """

    if not runs:
        raise ValueError(
            "At least one experiment run is required."
        )

    path = Path(file_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "experiment_name",
        "parameter_name",
        "parameter_value",
        "problem_seed",
        "ga_seed",
        "generation",
        "best_distance",
        "mean_distance",
    ]

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for run in runs:
            for stats in run.result.history:
                writer.writerow({
                    "experiment_name":
                        run.experiment_name,

                    "parameter_name":
                        run.parameter_name,

                    "parameter_value":
                        run.parameter_value,

                    "problem_seed":
                        run.problem_seed,

                    "ga_seed":
                        run.ga_seed,

                    "generation":
                        stats.generation,

                    "best_distance":
                        stats.best_distance,

                    "mean_distance":
                        stats.mean_distance,
                })