from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_c"
)

HISTORY_FILE = RESULTS_DIR / "history.csv"
PLOTS_DIR = RESULTS_DIR / "plots"

OUTPUT_FILE = (
    PLOTS_DIR
    / "convergence.png"
)

CHECKPOINTS = [
    50,
    100,
    200,
    500,
    1000,
]


def main() -> None:
    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    history = pd.read_csv(HISTORY_FILE)

    max_generations = int(
        history["parameter_value"].max()
    )

    longest_runs = history[
        history["parameter_value"]
        == max_generations
    ]

    convergence = (
        longest_runs.groupby("generation")
        .agg(
            mean_best_distance=(
                "best_distance",
                "mean",
            ),
            std_best_distance=(
                "best_distance",
                "std",
            ),
        )
        .reset_index()
    )

    plt.figure(figsize=(8, 5))

    line = plt.plot(
        convergence["generation"],
        convergence["mean_best_distance"],
        label="Mean best distance",
    )[0]

    plt.fill_between(
        convergence["generation"],
        (
            convergence["mean_best_distance"]
            - convergence["std_best_distance"]
        ),
        (
            convergence["mean_best_distance"]
            + convergence["std_best_distance"]
        ),
        alpha=0.2,
        color=line.get_color(),
        label="±1 standard deviation",
    )

    checkpoints = convergence[
        convergence["generation"].isin(
            CHECKPOINTS
        )
    ]

    plt.scatter(
        checkpoints["generation"],
        checkpoints["mean_best_distance"],
        color=line.get_color(),
        zorder=3,
        label="Tested generation counts",
    )

    plt.xlabel("Generation")
    plt.ylabel("Mean best tour distance")
    plt.title(
        "Convergence Across Generations"
    )

    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        OUTPUT_FILE,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Plot saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
