import csv
from dataclasses import replace

import pytest

from src.config import BASELINE
from src.experiment import run_experiment_repeated
from src.export_csv import (
    export_history_csv,
    export_runs_csv,
)


def test_export_runs_csv(tmp_path):
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    runs = run_experiment_repeated(
        experiment_name="B",
        parameter_name="population_size",
        config=config,
        problem_seed=123,
        ga_seeds=[0, 1, 2],
    )

    file_path = tmp_path / "runs.csv"

    export_runs_csv(
        runs,
        file_path,
    )

    with file_path.open(
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(
            csv.DictReader(file)
        )

    assert len(rows) == 3

    assert rows[0]["experiment_name"] == "B"

    assert (
        rows[0]["parameter_name"]
        == "population_size"
    )

    assert int(
        rows[0]["population_size"]
    ) == 20


def test_export_history_csv(tmp_path):
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    runs = run_experiment_repeated(
        experiment_name="C",
        parameter_name="generations",
        config=config,
        problem_seed=123,
        ga_seeds=[0, 1],
    )

    file_path = tmp_path / "history.csv"

    export_history_csv(
        runs,
        file_path,
    )

    with file_path.open(
        newline="",
        encoding="utf-8",
    ) as file:
        rows = list(
            csv.DictReader(file)
        )

    # generation 0 through generation 5
    # = 6 rows per run
    # 2 runs => 12 rows

    assert len(rows) == 12

def test_export_runs_requires_data(tmp_path):
    file_path = tmp_path / "runs.csv"

    with pytest.raises(ValueError):
        export_runs_csv(
            [],
            file_path,
        )

def test_export_creates_parent_directories(
    tmp_path,
):
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=2,
    )

    runs = run_experiment_repeated(
        experiment_name="D",
        parameter_name="mutation_rate",
        config=config,
        problem_seed=123,
        ga_seeds=[0],
    )

    file_path = (
        tmp_path
        / "results"
        / "experiment_d"
        / "runs.csv"
    )

    export_runs_csv(
        runs,
        file_path,
    )

    assert file_path.exists()