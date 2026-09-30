from pathlib import Path

from src.config import BASELINE
from src.experiment import run_parameter_sweep
from src.export_csv import (
    export_runs_csv,
    export_history_csv,
)


# ---------------------------------------------------------
# Experiment B - Smoke test
# ---------------------------------------------------------

# Independent variable:
# Population size.
POPULATION_VALUES = [
    50,
    100,
    200,
    500,
    1000,
]

# Keep the TSP problem fixed.
PROBLEM_SEED = 12345

GA_SEEDS = list(range(30)) # Run 30 different GA instances


# ---------------------------------------------------------
# Output paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_b"
)

RUNS_FILE = RESULTS_DIR / "runs.csv"
HISTORY_FILE = RESULTS_DIR / "history.csv"


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main() -> None:
    sweep = run_parameter_sweep(
        experiment_name="B",
        parameter_name="population_size",
        values=POPULATION_VALUES,
        baseline=BASELINE,
        problem_seed=PROBLEM_SEED,
        ga_seeds=GA_SEEDS,
    )

    export_runs_csv(
        runs=sweep.runs,
        file_path=RUNS_FILE,
    )

    export_history_csv(
        runs=sweep.runs,
        file_path=HISTORY_FILE,
    )

    print("Experiment B smoke test completed.")
    print(f"Total runs: {len(sweep.runs)}")
    print(f"Runs saved to: {RUNS_FILE}")
    print(f"History saved to: {HISTORY_FILE}")


if __name__ == "__main__":
    main()