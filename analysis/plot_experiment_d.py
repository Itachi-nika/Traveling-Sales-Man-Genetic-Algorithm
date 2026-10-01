import csv
from pathlib import Path

import matplotlib.pyplot as plt


# File paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "results"
    / "experiment_d"
    / "summaries.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_d"
    / "plots"
)


def main():

    mutation_rates = []
    mean_distances = []
    std_distances = []
    mean_runtimes = []
    std_runtimes = []

    # Read summary statistics
    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            mutation_rates.append(
                float(row["mutation_rate"])
            )

            mean_distances.append(
                float(row["mean_best_distance"])
            )

            std_distances.append(
                float(row["std_best_distance"])
            )

            mean_runtimes.append(
                float(row["mean_runtime_seconds"])
            )

            std_runtimes.append(
                float(row["std_runtime_seconds"])
            )

    if not mutation_rates:
        raise ValueError("No summary data found.")

    # Create output directory
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    positions = range(len(mutation_rates))

    labels = [
        f"{rate:.2f}"
        for rate in mutation_rates
    ]

    # ---------------------------------
    # Diagram 1: Solution quality
    # ---------------------------------

    plt.figure(figsize=(9, 6))

    plt.errorbar(
        positions,
        mean_distances,
        yerr=std_distances,
        fmt="o-",
        capsize=5,
        linewidth=2,
    )

    plt.xticks(
        positions,
        labels,
    )

    plt.xlabel("Mutation rate")
    plt.ylabel("Mean best distance")

    plt.title(
        "Experiment D: Mutation Rate vs Solution Quality"
    )

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.tight_layout()

    distance_output_file = (
        OUTPUT_DIR
        / "mutation_vs_distance.png"
    )

    plt.savefig(
        distance_output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"Distance plot saved in: {distance_output_file}"
    )

    # ---------------------------------
    # Diagram 2: Runtime
    # ---------------------------------

    plt.figure(figsize=(9, 6))

    plt.errorbar(
        positions,
        mean_runtimes,
        yerr=std_runtimes,
        fmt="o-",
        capsize=5,
        linewidth=2,
    )

    plt.xticks(
        positions,
        labels,
    )

    plt.xlabel("Mutation rate")
    plt.ylabel("Mean runtime (seconds)")

    plt.title(
        "Experiment D: Mutation Rate vs Runtime"
    )

    plt.grid(
        True,
        alpha=0.3,
    )

    plt.tight_layout()

    runtime_output_file = (
        OUTPUT_DIR
        / "mutation_vs_runtime.png"
    )

    plt.savefig(
        runtime_output_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(
        f"Runtime plot saved in: {runtime_output_file}"
    )

    print("All plots created successfully.")


if __name__ == "__main__":
    main()