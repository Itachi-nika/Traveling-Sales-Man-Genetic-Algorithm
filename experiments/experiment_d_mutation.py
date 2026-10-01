from pathlib import Path
from dataclasses import replace

from src.config import BASELINE
from src.experiment import run_experiment_once
from src.export_csv import export_runs_csv, export_history_csv


# Experiment D: Mutation rate

MUTATION_VALUES = [0.00, 0.01, 0.05, 0.10, 0.20, 0.50]

PROBLEM_SEED = 12345

GA_SEEDS = list(range(30))


def main():

    all_runs = []

    total_runs = len(MUTATION_VALUES) * len(GA_SEEDS)
    completed_runs = 0

    for mutation_rate in MUTATION_VALUES:

        config = replace(
            BASELINE,
            mutation_rate=mutation_rate,
        )

        for ga_seed in GA_SEEDS:

            print(
                f"Starting run {completed_runs + 1}/{total_runs} "
                f"| Mutation: {mutation_rate} "
                f"| Seed: {ga_seed}",
                flush=True,
            )

            run = run_experiment_once(
                experiment_name="D",
                parameter_name="mutation_rate",
                config=config,
                problem_seed=PROBLEM_SEED,
                ga_seed=ga_seed,
            )

            all_runs.append(run)

            completed_runs += 1

            progress = (completed_runs / total_runs) * 100

            print(
                f"Progress: {progress:.1f}% "
                f"({completed_runs}/{total_runs})\n",
                flush=True,
            )

    # Export results
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "results" / "experiment_d"

    export_runs_csv(
        all_runs,
        output_dir / "runs.csv",
    )

    export_history_csv(
        all_runs,
        output_dir / "history.csv",
    )

    print("Experiment D completed.")
    print(f"Results saved in: {output_dir}")


if __name__ == "__main__":
    main()