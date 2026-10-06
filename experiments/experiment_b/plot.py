from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RUNS_FILE = (
    PROJECT_ROOT
    / "results"
    / "experiment_b"
    / "runs.csv"
)

HISTORY_FILE = (
    PROJECT_ROOT
    / "results"
    / "experiment_b"
    / "history.csv"
)

PLOTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_b"
    / "plots"
)




BEST_DISTANCE_OUTPUT_FILE = (
    PLOTS_DIR
    / "population_vs_best_distance.png"
)

RUNTIME_OUTPUT_FILE = (
    PLOTS_DIR
    / "population_vs_runtime.png"
)

CONVERGENCE_OUTPUT_FILE = (
    PLOTS_DIR
    / "population_convergence.png"
)

BOXPLOT_OUTPUT_FILE = (
    PLOTS_DIR
    / "population_best_distance_boxplot.png"
)


def main() -> None:



    runs_df = pd.read_csv(RUNS_FILE)
    history_df = pd.read_csv(HISTORY_FILE)

    
    runs_df.columns = runs_df.columns.str.strip()
    history_df.columns = history_df.columns.str.strip()

    
    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -----------------------------------------------------
    # Graph 1:
    # Population size vs mean best distance
    # -----------------------------------------------------

    best_distance_summary = (
        runs_df
        .groupby("population_size")["best_distance"]
        .agg(["mean", "std"])
        .reset_index()
    )

    print("Best distance summary:")
    print(best_distance_summary)
    print()

    plt.figure(figsize=(8, 5))

    plt.errorbar(
        best_distance_summary["population_size"],
        best_distance_summary["mean"],
        yerr=best_distance_summary["std"],
        marker="o",
        capsize=5,
    )

    plt.xlabel("Population size")
    plt.ylabel("Mean best distance")

    plt.title(
        "Effect of Population Size on Solution Quality"
    )

    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        BEST_DISTANCE_OUTPUT_FILE,
        dpi=300,
    )

    # -----------------------------------------------------
    # Graph 2:
    # Population size vs mean runtime
    # -----------------------------------------------------

    runtime_summary = (
        runs_df
        .groupby("population_size")["runtime_seconds"]
        .agg(["mean", "std"])
        .reset_index()
    )

    print("Runtime summary:")
    print(runtime_summary)
    print()

    plt.figure(figsize=(8, 5))

    plt.errorbar(
        runtime_summary["population_size"],
        runtime_summary["mean"],
        yerr=runtime_summary["std"],
        marker="o",
        capsize=5,
    )

    plt.xlabel("Population size")
    plt.ylabel("Mean runtime (seconds)")

    plt.title(
        "Effect of Population Size on Runtime"
    )

    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        RUNTIME_OUTPUT_FILE,
        dpi=300,
    )

    # -----------------------------------------------------
    # Graph 3:
    # Convergence over generations
    # -----------------------------------------------------

    convergence_summary = (
        history_df
        .groupby(
            [
                "parameter_value",
                "generation",
            ]
        )["best_distance"]
        .mean()
        .reset_index()
    )

    print("Convergence summary:")
    print(convergence_summary.head())
    print()

    plt.figure(figsize=(9, 6))

    population_values = sorted(
        convergence_summary[
            "parameter_value"
        ].unique()
    )

    for population_size in population_values:

        population_data = (
            convergence_summary[
                convergence_summary[
                    "parameter_value"
                ]
                == population_size
            ]
        )

        plt.plot(
            population_data["generation"],
            population_data["best_distance"],
            label=f"Population {population_size}",
        )

    plt.xlabel("Generation")
    plt.ylabel("Mean best distance")

    plt.title(
        "Convergence for Different Population Sizes"
    )

    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        CONVERGENCE_OUTPUT_FILE,
        dpi=300,
    )

    # -----------------------------------------------------
    # Graph 4:
    # Distribution of final best distances
    # -----------------------------------------------------

    population_values = sorted(
        runs_df["population_size"].unique()
    )

    boxplot_data = []

    for population_size in population_values:

        distances = runs_df[
            runs_df["population_size"]
            == population_size
        ]["best_distance"]

        boxplot_data.append(distances)

    plt.figure(figsize=(8, 5))

    plt.boxplot(
        boxplot_data,
        tick_labels=[
            str(value)
            for value in population_values
        ],
    )

    plt.xlabel("Population size")
    plt.ylabel("Best distance")

    plt.title(
        "Distribution of Best Distance "
        "for Different Population Sizes"
    )

    plt.grid(
        axis="y",
        alpha=0.3,
    )

    plt.tight_layout()

    plt.savefig(
        BOXPLOT_OUTPUT_FILE,
        dpi=300,
    )

  
    print("Plots saved:")
    print(BEST_DISTANCE_OUTPUT_FILE)
    print(RUNTIME_OUTPUT_FILE)
    print(CONVERGENCE_OUTPUT_FILE)
    print(BOXPLOT_OUTPUT_FILE)

    # Display all created figures.
    plt.show()


if __name__ == "__main__":
    main()