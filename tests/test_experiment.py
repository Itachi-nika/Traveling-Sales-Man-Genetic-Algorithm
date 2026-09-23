from dataclasses import replace

import pytest

from src.config import BASELINE
from src.experiment import (
    run_experiment_once,
    run_experiment_repeated,
    summarize_experiment_runs,
    run_parameter_sweep,
)


def test_experiment_run_contains_correct_metadata():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=30,
        generations=5,
    )

    run = run_experiment_once(
        experiment_name="B",
        parameter_name="population_size",
        config=config,
        problem_seed=123,
        ga_seed=42,
    )

    assert run.experiment_name == "B"
    assert run.parameter_name == "population_size"
    assert run.parameter_value == 30

    assert run.problem_seed == 123
    assert run.ga_seed == 42

    assert run.config == config

def test_experiment_run_contains_ga_result():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    run = run_experiment_once(
        experiment_name="C",
        parameter_name="generations",
        config=config,
        problem_seed=123,
        ga_seed=42,
    )

    assert run.result.best_distance > 0
    assert run.result.runtime_seconds >= 0
    assert run.result.population_evaluations == 20 * 6

def test_unknown_parameter_name_raises_error():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    with pytest.raises(ValueError):
        run_experiment_once(
            experiment_name="X",
            parameter_name="does_not_exist",
            config=config,
            problem_seed=123,
            ga_seed=42,
        )

def test_empty_experiment_name_raises_error():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    with pytest.raises(ValueError):
        run_experiment_once(
            experiment_name="",
            parameter_name="population_size",
            config=config,
            problem_seed=123,
            ga_seed=42,
        )

def test_repeated_experiment_has_correct_number_of_runs():
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
        ga_seeds=[0, 1, 2, 3],
    )

    assert len(runs) == 4

def test_repeated_experiment_uses_correct_ga_seeds():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    seeds = [10, 20, 30]

    runs = run_experiment_repeated(
        experiment_name="C",
        parameter_name="generations",
        config=config,
        problem_seed=123,
        ga_seeds=seeds,
    )

    result_seeds = [
        run.ga_seed
        for run in runs
    ]

    assert result_seeds == seeds

def test_repeated_experiment_uses_same_problem_seed():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    runs = run_experiment_repeated(
        experiment_name="A",
        parameter_name="num_cities",
        config=config,
        problem_seed=999,
        ga_seeds=[0, 1, 2],
    )

    for run in runs:
        assert run.problem_seed == 999

def test_empty_ga_seed_list_raises_error():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    with pytest.raises(ValueError):
        run_experiment_repeated(
            experiment_name="B",
            parameter_name="population_size",
            config=config,
            problem_seed=123,
            ga_seeds=[],
        )

def test_duplicate_ga_seeds_raise_error():
    config = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    with pytest.raises(ValueError):
        run_experiment_repeated(
            experiment_name="B",
            parameter_name="population_size",
            config=config,
            problem_seed=123,
            ga_seeds=[1, 2, 2, 3],
        )

def test_experiment_summary_has_correct_metadata():
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

    summary = summarize_experiment_runs(runs)

    assert summary.experiment_name == "B"
    assert summary.parameter_name == "population_size"
    assert summary.parameter_value == 20
    assert summary.num_runs == 3

def test_experiment_summary_distance_statistics():
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

    summary = summarize_experiment_runs(runs)

    distances = [
        run.result.best_distance
        for run in runs
    ]

    assert summary.mean_best_distance == pytest.approx(
        sum(distances) / len(distances)
    )

    assert summary.min_best_distance == pytest.approx(
        min(distances)
    )

    assert summary.max_best_distance == pytest.approx(
        max(distances)
    )

def test_experiment_summary_median():
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
        ga_seeds=[0, 1, 2],
    )

    summary = summarize_experiment_runs(runs)

    distances = sorted(
        run.result.best_distance
        for run in runs
    )

    assert summary.median_best_distance == pytest.approx(
        distances[1]
    )

def test_single_run_summary_has_zero_standard_deviation():
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
        ga_seeds=[42],
    )

    summary = summarize_experiment_runs(runs)

    assert summary.std_best_distance == 0.0
    assert summary.std_runtime_seconds == 0.0

def test_empty_run_list_cannot_be_summarized():
    with pytest.raises(ValueError):
        summarize_experiment_runs([])

def test_different_parameter_values_cannot_be_summarized():
    config_1 = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
    )

    config_2 = replace(
        BASELINE,
        num_cities=10,
        population_size=30,
        generations=5,
    )

    run_1 = run_experiment_once(
        experiment_name="B",
        parameter_name="population_size",
        config=config_1,
        problem_seed=123,
        ga_seed=1,
    )

    run_2 = run_experiment_once(
        experiment_name="B",
        parameter_name="population_size",
        config=config_2,
        problem_seed=123,
        ga_seed=2,
    )

    with pytest.raises(ValueError):
        summarize_experiment_runs(
            [run_1, run_2]
        )

def test_parameter_sweep_has_correct_number_of_runs():
    baseline = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=3,
    )

    sweep = run_parameter_sweep(
        experiment_name="B",
        parameter_name="population_size",
        values=[10, 20, 30],
        baseline=baseline,
        problem_seed=123,
        ga_seeds=[0, 1],
    )

    assert len(sweep.runs) == 6

def test_parameter_sweep_has_one_summary_per_value():
    baseline = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=3,
    )

    sweep = run_parameter_sweep(
        experiment_name="B",
        parameter_name="population_size",
        values=[10, 20, 30],
        baseline=baseline,
        problem_seed=123,
        ga_seeds=[0, 1],
    )

    assert len(sweep.summaries) == 3

    values = [
        summary.parameter_value
        for summary in sweep.summaries
    ]

    assert values == [10, 20, 30]

def test_parameter_sweep_preserves_other_baseline_values():
    baseline = replace(
        BASELINE,
        num_cities=10,
        population_size=20,
        generations=5,
        mutation_rate=0.05,
    )

    sweep = run_parameter_sweep(
        experiment_name="B",
        parameter_name="population_size",
        values=[10, 30],
        baseline=baseline,
        problem_seed=123,
        ga_seeds=[0],
    )

    for run in sweep.runs:
        assert run.config.num_cities == 10
        assert run.config.generations == 5
        assert run.config.mutation_rate == 0.05

def test_parameter_sweep_requires_values():
    with pytest.raises(ValueError):
        run_parameter_sweep(
            experiment_name="B",
            parameter_name="population_size",
            values=[],
            baseline=BASELINE,
            problem_seed=123,
            ga_seeds=[0],
        )

def test_parameter_sweep_rejects_duplicate_values():
    with pytest.raises(ValueError):
        run_parameter_sweep(
            experiment_name="B",
            parameter_name="population_size",
            values=[50, 100, 100],
            baseline=BASELINE,
            problem_seed=123,
            ga_seeds=[0],
        )