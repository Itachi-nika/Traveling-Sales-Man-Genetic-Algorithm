from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_c"
)

SUMMARY_FILE = RESULTS_DIR / "summaries.csv"

OUTPUT_FILE = (
    RESULTS_DIR
    / "experiment_c_table.tex"
)


def main() -> None:
    summary = pd.read_csv(SUMMARY_FILE)

    summary = summary.sort_values(
        "generations"
    ).reset_index(drop=True)

    improvements = ["--"]

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
            f"{improvement:.1f}\\%"
        )

    rows = []

    for i, row in summary.iterrows():
        generations = int(
            row["generations"]
        )

        mean_distance = (
            row["mean_best_distance"]
        )

        std_distance = (
            row["std_best_distance"]
        )

        runtime = (
            row["mean_runtime_seconds"]
        )

        improvement = improvements[i]

        rows.append(
            f"{generations} & "
            f"{mean_distance:.2f} "
            f"$\\pm$ {std_distance:.2f} & "
            f"{runtime:.2f} & "
            f"{improvement} \\\\"
        )

    table = "\n".join([
        "\\begin{table}[h]",
        "\\centering",
        "\\caption{Effect of the number of generations on solution quality and runtime.}",
        "\\label{tab:experiment-c}",
        "\\begin{tabular}{rrrr}",
        "\\hline",
        "Generations & Mean best distance & Runtime (s) & Improvement \\\\",
        "\\hline",
        *rows,
        "\\hline",
        "\\end{tabular}",
        "\\end{table}",
    ])

    OUTPUT_FILE.write_text(
        table,
        encoding="utf-8",
    )

    print(
        f"Table saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()