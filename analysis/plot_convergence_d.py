import csv
import statistics
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt


# File paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "results"
    / "experiment_d"
    / "history.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_d"
    / "plots"
)


def main():

    # Group distances by mutation rate and generation
    grouped_data = defaultdict(
        lambda: defaultdict(list)
    )

    # Read experimental history
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
                row["parameter_value"]
            )

            generation = int(
                row["generation"]
            )

            best_distance = float(
                row["best_distance"]
            )

            grouped_data[mutation_rate][generation].append(
                best_distance
            )

    if not grouped_data:
        raise ValueError("No history data found.")

    # Create output directory
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Create convergence plot
    plt.figure(figsize=(10, 6))

    for mutation_rate in sorted(grouped_data):

        generations = sorted(
            grouped_data[mutation_rate]
        )

        mean_distances = [
            statistics.mean(
                grouped_data[mutation_rate][generation]
            )
            for generation in generations
        ]

        plt.plot(
            generations,
            mean_distances,
            label=f"Mutation {mutation_rate:.2f}",
            linewidth=2,
        )

    plt.xlabel("Generation")
    plt.ylabel("Mean best distance")

    plt.title(
        "Experiment D: Convergence by Mutation Rate"
    )

    plt.legend(
        title="Mutation rate"
    )

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.tight_layout()

    # Save convergence plot
    output_file = (
        OUTPUT_DIR
        / "mutation_convergence.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print("Convergence plot created successfully.")
    print(f"Saved in: {output_file}")


if __name__ == "__main__":
    main()