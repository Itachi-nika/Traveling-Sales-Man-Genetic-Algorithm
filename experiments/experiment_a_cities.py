from pathlib import Path

from src.config import BASELINE
from src.experiment import run_parameter_sweep
from src.export_csv import (
    export_runs_csv,
    export_history_csv,
)


# ---------------------------------------------------------
# Experiment A - Number of Cities
# ---------------------------------------------------------

# Independent variable.
# Only the number of cities changes in this experiment.
CITY_VALUES = [
    20,
    50,
    100,
    200,
    500,
]

# Fixed TSP problem seed.
#
# We deliberately keep this constant so that the
# experiment studies increasing problem size on the
# same deterministic problem family.
PROBLEM_SEED = 12345

# 30 independent stochastic GA runs for each city size.
GA_SEEDS = list(range(30))


# ---------------------------------------------------------
# Output paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_a"
)

RUNS_FILE = RESULTS_DIR / "runs.csv"
HISTORY_FILE = RESULTS_DIR / "history.csv"


# ---------------------------------------------------------
# Main experiment
# ---------------------------------------------------------

def main() -> None:

    # Run the parameter sweep.
    # The parameter sweep creates a new GAConfig for each
    # city value while preserving all remaining BASELINE
    # parameters.
    sweep = run_parameter_sweep(
        experiment_name="A",
        parameter_name="num_cities",
        values=CITY_VALUES,
        baseline=BASELINE,
        problem_seed=PROBLEM_SEED,
        ga_seeds=GA_SEEDS,
    )

    # -----------------------------------------------------
    # Export raw run-level results
    # -----------------------------------------------------

    export_runs_csv(
        runs=sweep.runs,
        file_path=RUNS_FILE,
    )

    # -----------------------------------------------------
    # Export generation-level convergence history
    # -----------------------------------------------------

    export_history_csv(
        runs=sweep.runs,
        file_path=HISTORY_FILE,
    )

    

    print("Experiment A completed.")
    

if __name__ == "__main__":
    main()