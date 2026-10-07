import csv
import statistics
from pathlib import Path
from collections import defaultdict


# File paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "results" / "experiment_d" / "runs.csv"

OUTPUT_FILE = PROJECT_ROOT / "results" / "experiment_d" / "summaries.csv"


def main():

    # Group results by mutation rate
    grouped_runs = defaultdict(list)

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            # Remove extra spaces
            row = {
                key.strip(): value.strip()
                for key, value in row.items()
            }

            mutation_rate = float(
                row["mutation_rate"]
            )

            grouped_runs[mutation_rate].append(row)

    if not grouped_runs:
        raise ValueError("No experimental data found.")

    summaries = []

    # Calculate statistics
    for mutation_rate in sorted(grouped_runs):

        runs = grouped_runs[mutation_rate]

        distances = [
            float(run["best_distance"])
            for run in runs
        ]

        runtimes = [
            float(run["runtime_seconds"])
            for run in runs
        ]

        summary = {
            "mutation_rate": mutation_rate,
            "num_runs": len(runs),

            "mean_best_distance":
                statistics.mean(distances),

            "median_best_distance":
                statistics.median(distances),

            "std_best_distance":
                statistics.stdev(distances)
                if len(distances) > 1 else 0.0,

            "min_best_distance":
                min(distances),

            "max_best_distance":
                max(distances),

            "mean_runtime_seconds":
                statistics.mean(runtimes),

            "std_runtime_seconds":
                statistics.stdev(runtimes)
                if len(runtimes) > 1 else 0.0,
        }

        summaries.append(summary)

    # Save summary statistics
    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=summaries[0].keys(),
        )

        writer.writeheader()
        writer.writerows(summaries)

    print("Experiment D analysis completed.")
    print(f"Summaries saved in: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()