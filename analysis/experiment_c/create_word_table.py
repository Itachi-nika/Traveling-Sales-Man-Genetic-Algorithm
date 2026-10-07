from pathlib import Path

import pandas as pd
from docx import Document


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_c"
)

SUMMARY_FILE = RESULTS_DIR / "summaries.csv"

OUTPUT_FILE = (
    RESULTS_DIR
    / "experiment_c_table.docx"
)


def main() -> None:
    summary = pd.read_csv(SUMMARY_FILE)

    summary = summary.sort_values(
        "generations"
    ).reset_index(drop=True)

    improvements = ["–"]

    for i in range(1, len(summary)):
        previous_distance = summary.loc[
            i - 1,
            "mean_best_distance",
        ]

        current_distance = summary.loc[
            i,
            "mean_best_distance",
        ]

        improvement = (
            (
                previous_distance
                - current_distance
            )
            / previous_distance
            * 100
        )

        improvements.append(
            f"{improvement:.1f}%"
        )

    document = Document()

    table = document.add_table(
        rows=1,
        cols=4,
    )

    table.style = "Table Grid"

    headers = [
        "Generations",
        "Mean best distance",
        "Runtime (s)",
        "Improvement",
    ]

    for i, header in enumerate(headers):
        table.rows[0].cells[i].text = header

    for i, row in summary.iterrows():
        cells = table.add_row().cells

        cells[0].text = str(
            int(row["generations"])
        )

        cells[1].text = (
            f'{row["mean_best_distance"]:.2f} '
            f'± {row["std_best_distance"]:.2f}'
        )

        cells[2].text = (
            f'{row["mean_runtime_seconds"]:.2f}'
        )

        cells[3].text = improvements[i]

    document.save(OUTPUT_FILE)

    print(
        f"Word table saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()