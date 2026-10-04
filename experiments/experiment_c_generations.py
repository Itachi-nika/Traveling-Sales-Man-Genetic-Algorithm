from dataclasses import replace
from pathlib import Path

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from src.config import BASELINE
from src.experiment import (
    run_experiment_once,
    summarize_experiment_runs,
)
from src.export_csv import (
    export_runs_csv,
    export_history_csv,
)

GENERATION_VALUES = [
    50,
    100,
    200,
    500,
    1000,
]

PROBLEM_SEED = 12345
GA_SEEDS = list(range(30))


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
    / "experiment_c"
)

RUNS_FILE = RESULTS_DIR / "runs.csv"
HISTORY_FILE = RESULTS_DIR / "history.csv"


def main() -> None:
    all_runs = []

    total_runs = (
        len(GENERATION_VALUES)
        * len(GA_SEEDS)
    )

    with Progress(
        SpinnerColumn(),
        TextColumn(
            "[bold]Experiment C[/bold]"
        ),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn(
            "Generations: {task.fields[generations]}"
        ),
        TextColumn(
            "Seed: {task.fields[seed]}"
        ),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
    ) as progress:

        task = progress.add_task(
            "Running",
            total=total_runs,
            generations="-",
            seed="-",
        )

        for generations in GENERATION_VALUES:
            config = replace(
                BASELINE,
                generations=generations,
            )

            runs = []

            for ga_seed in GA_SEEDS:
                progress.update(
                    task,
                    generations=generations,
                    seed=ga_seed,
                )

                run = run_experiment_once(
                    experiment_name="C",
                    parameter_name="generations",
                    config=config,
                    problem_seed=PROBLEM_SEED,
                    ga_seed=ga_seed,
                )

                runs.append(run)
                all_runs.append(run)

                progress.advance(task)

            summarize_experiment_runs(runs)

    export_runs_csv(
        runs=all_runs,
        file_path=RUNS_FILE,
    )

    export_history_csv(
        runs=all_runs,
        file_path=HISTORY_FILE,
    )

    print("Experiment C completed.")


if __name__ == "__main__":
    main()