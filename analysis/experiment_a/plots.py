import csv
from pathlib import Path

import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_a"
)

SUMMARY_FILE = RESULTS_DIR / "summaries.csv"

PLOTS_DIR = RESULTS_DIR / "plots"

GEN95_PNG = (
    PLOTS_DIR
    / "generation_to_95pct.png"
)

GEN95_PDF = (
    PLOTS_DIR
    / "generation_to_95pct.pdf"
)


def main() -> None:
    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    num_cities = []
    mean_generation_95pct = []

    with SUMMARY_FILE.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            num_cities.append(
                int(row["num_cities"])
            )

            mean_generation_95pct.append(
                float(
                    row["mean_generation_95pct"]
                )
            )

    plt.figure(figsize=(7, 4.5))

    plt.plot(
        num_cities,
        mean_generation_95pct,
        marker="o",
    )

    plt.xlabel("Number of Cities")
    plt.ylabel("Mean Generation to 95% Improvement")
    plt.title("Convergence Speed vs Problem Size")
    plt.xticks(num_cities)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        GEN95_PNG,
        dpi=300,
        bbox_inches="tight",
    )

    plt.savefig(
        GEN95_PDF,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Plot saved to: {GEN95_PNG}")
    print(f"Plot saved to: {GEN95_PDF}")


if __name__ == "__main__":
    main()