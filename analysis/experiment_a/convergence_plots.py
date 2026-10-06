import csv
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_a"
)

HISTORY_FILE = RESULTS_DIR / "history.csv"

PLOTS_DIR = RESULTS_DIR / "plots"

CITY_VALUES = [
    100,
    200,
    500,
]


def main() -> None:
    PLOTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    data = defaultdict(
        lambda: defaultdict(
            lambda: {
                "best": [],
                "mean": [],
            }
        )
    )

    with HISTORY_FILE.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            num_cities = int(
                float(row["parameter_value"])
            )

            if num_cities not in CITY_VALUES:
                continue

            generation = int(
                row["generation"]
            )

            best_distance = float(
                row["best_distance"]
            )

            mean_distance = float(
                row["mean_distance"]
            )

            data[num_cities][generation][
                "best"
            ].append(best_distance)

            data[num_cities][generation][
                "mean"
            ].append(mean_distance)

    for num_cities in CITY_VALUES:

        generations = sorted(
            data[num_cities].keys()
        )

        mean_best_distances = []
        mean_population_distances = []

        for generation in generations:

            generation_data = (
                data[num_cities][generation]
            )

            mean_best_distances.append(
                statistics.mean(
                    generation_data["best"]
                )
            )

            mean_population_distances.append(
                statistics.mean(
                    generation_data["mean"]
                )
            )

        plt.figure(
            figsize=(7, 4.5)
        )

        plt.plot(
            generations,
            mean_best_distances,
            label="Best Distance",
        )

        plt.plot(
            generations,
            mean_population_distances,
            label="Mean Population Distance",
        )

        plt.xlabel(
            "Generation"
        )

        plt.ylabel(
            "Mean Tour Distance"
        )

        plt.title(
            f"GA Convergence - {num_cities} Cities"
        )

        plt.grid(
            alpha=0.3
        )

        plt.legend()

        plt.tight_layout()

        png_file = (
            PLOTS_DIR
            / f"convergence_{num_cities}.png"
        )

        pdf_file = (
            PLOTS_DIR
            / f"convergence_{num_cities}.pdf"
        )

        plt.savefig(
            png_file,
            dpi=300,
            bbox_inches="tight",
        )

        plt.savefig(
            pdf_file,
            bbox_inches="tight",
        )

        plt.close()

        print(
            f"Saved: {png_file}"
        )


if __name__ == "__main__":
    main()