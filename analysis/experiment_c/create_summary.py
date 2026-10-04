from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_c"
)

RUNS_FILE = RESULTS_DIR / "runs.csv"
SUMMARY_FILE = RESULTS_DIR / "summaries.csv"


def main() -> None:
    runs = pd.read_csv(RUNS_FILE)

    runs["improvement_percent"] = (
        (
            runs["initial_best_distance"]
            - runs["best_distance"]
        )
        / runs["initial_best_distance"]
        * 100
    )

    summary = (
        runs.groupby("parameter_value")
        .agg(
            num_runs=("best_distance", "count"),
            mean_best_distance=("best_distance", "mean"),
            median_best_distance=("best_distance", "median"),
            std_best_distance=("best_distance", "std"),
            min_best_distance=("best_distance", "min"),
            max_best_distance=("best_distance", "max"),
            mean_runtime_seconds=("runtime_seconds", "mean"),
            std_runtime_seconds=("runtime_seconds", "std"),
            mean_improvement_percent=(
                "improvement_percent",
                "mean",
            ),
            std_improvement_percent=(
                "improvement_percent",
                "std",
            ),
        )
        .reset_index()
        .rename(
            columns={
                "parameter_value": "generations",
            }
        )
        .sort_values("generations")
    )

    summary.to_csv(
        SUMMARY_FILE,
        index=False,
    )

    print(f"Summary saved to: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
