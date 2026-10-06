import csv
import statistics
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_a"
)

RUNS_FILE = RESULTS_DIR / "runs.csv"
HISTORY_FILE = RESULTS_DIR / "history.csv"
SUMMARY_FILE = RESULTS_DIR / "summaries.csv"


def read_csv(file_path: Path) -> list[dict[str, str]]:
    with file_path.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        return list(csv.DictReader(file))


def calculate_generation_95pct(
    initial_distance: float,
    final_distance: float,
    history_rows: list[dict[str, str]],
) -> int:
    """
    Return the first generation where 95% of the
    total achieved improvement has been reached.
    """

    total_improvement = (
        initial_distance - final_distance
    )

    if total_improvement <= 0:
        return 0

    target_distance = (
        initial_distance
        - 0.95 * total_improvement
    )

    sorted_history = sorted(
        history_rows,
        key=lambda row: int(row["generation"]),
    )

    for row in sorted_history:
        if float(row["best_distance"]) <= target_distance:
            return int(row["generation"])

    return int(
        sorted_history[-1]["generation"]
    )


def main() -> None:
    runs = read_csv(RUNS_FILE)
    history = read_csv(HISTORY_FILE)

    runs_by_cities: dict[
        int,
        list[dict[str, str]],
    ] = {}

    for run in runs:
        num_cities = int(run["num_cities"])

        runs_by_cities.setdefault(
            num_cities,
            [],
        ).append(run)

    history_by_run: dict[
        tuple[int, int],
        list[dict[str, str]],
    ] = {}

    for row in history:
        num_cities = int(
            float(row["parameter_value"])
        )
        ga_seed = int(row["ga_seed"])

        key = (
            num_cities,
            ga_seed,
        )

        history_by_run.setdefault(
            key,
            [],
        ).append(row)

    summary_rows = []

    for num_cities in sorted(runs_by_cities):
        city_runs = runs_by_cities[num_cities]

        initial_distances = []
        best_distances = []
        improvements = []
        runtimes = []
        generations_95pct = []

        for run in city_runs:
            initial_distance = float(
                run["initial_best_distance"]
            )

            best_distance = float(
                run["best_distance"]
            )

            runtime = float(
                run["runtime_seconds"]
            )

            improvement_pct = (
                (
                    initial_distance
                    - best_distance
                )
                / initial_distance
                * 100
            )

            ga_seed = int(
                run["ga_seed"]
            )

            history_rows = history_by_run[
                (
                    num_cities,
                    ga_seed,
                )
            ]

            generation_95pct = (
                calculate_generation_95pct(
                    initial_distance=initial_distance,
                    final_distance=best_distance,
                    history_rows=history_rows,
                )
            )

            initial_distances.append(
                initial_distance
            )

            best_distances.append(
                best_distance
            )

            improvements.append(
                improvement_pct
            )

            runtimes.append(
                runtime
            )

            generations_95pct.append(
                generation_95pct
            )

        first_run = city_runs[0]

        summary_rows.append(
            {
                "num_cities": num_cities,
                "num_runs": len(city_runs),
                "problem_seed": int(
                    first_run["problem_seed"]
                ),
                "population_size": int(
                    first_run["population_size"]
                ),
                "generations": int(
                    first_run["generations"]
                ),
                "crossover_rate": float(
                    first_run["crossover_rate"]
                ),
                "mutation_rate": float(
                    first_run["mutation_rate"]
                ),
                "tournament_size": int(
                    first_run["tournament_size"]
                ),
                "elitism": int(
                    first_run["elitism"]
                ),
                "mean_initial_best_distance":
                    statistics.mean(
                        initial_distances
                    ),
                "mean_best_distance":
                    statistics.mean(
                        best_distances
                    ),
                "median_best_distance":
                    statistics.median(
                        best_distances
                    ),
                "std_best_distance":
                    statistics.stdev(
                        best_distances
                    ),
                "min_best_distance":
                    min(best_distances),
                "max_best_distance":
                    max(best_distances),
                "mean_improvement_pct":
                    statistics.mean(
                        improvements
                    ),
                "std_improvement_pct":
                    statistics.stdev(
                        improvements
                    ),
                "mean_runtime_seconds":
                    statistics.mean(
                        runtimes
                    ),
                "std_runtime_seconds":
                    statistics.stdev(
                        runtimes
                    ),
                "mean_generation_95pct":
                    statistics.mean(
                        generations_95pct
                    ),
                "median_generation_95pct":
                    statistics.median(
                        generations_95pct
                    ),
            }
        )

    fieldnames = list(
        summary_rows[0].keys()
    )

    with SUMMARY_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(summary_rows)

    print(
        f"Summary saved to: {SUMMARY_FILE}"
    )


if __name__ == "__main__":
    main()