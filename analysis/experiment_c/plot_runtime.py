from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_c"
)

SUMMARY_FILE = RESULTS_DIR / "summaries.csv"
PLOTS_DIR = RESULTS_DIR / "plots"

OUTPUT_FILE = (
    PLOTS_DIR
    / "runtime_vs_generations.png"
)


def main() -> None:
    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary = pd.read_csv(SUMMARY_FILE)

    plt.figure(figsize=(8, 5))

    plt.errorbar(
        summary["generations"],
        summary["mean_runtime_seconds"],
        yerr=summary["std_runtime_seconds"],
        marker="o",
        capsize=4,
    )

    plt.xlabel("Number of generations")
    plt.ylabel("Mean runtime (seconds)")
    plt.title(
        "Runtime vs Number of Generations"
    )

    plt.grid(alpha=0.3)
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
