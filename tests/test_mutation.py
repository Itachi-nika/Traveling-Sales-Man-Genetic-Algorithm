import random

import pytest

from src.mutation import swap_mutation


def test_mutation_produces_valid_permutation():
    individual = [0, 1, 2, 3, 4, 5]

    rng = random.Random(42)

    mutated = swap_mutation(
        individual,
        rng,
    )

    assert sorted(mutated) == list(range(6))


def test_mutation_preserves_length():
    individual = [0, 1, 2, 3, 4, 5]

    rng = random.Random(42)

    mutated = swap_mutation(
        individual,
        rng,
    )

    assert len(mutated) == len(individual)


def test_mutation_changes_individual():
    individual = [0, 1, 2, 3, 4, 5]

    rng = random.Random(42)

    mutated = swap_mutation(
        individual,
        rng,
    )

    assert mutated != individual


def test_mutation_does_not_modify_original():
    individual = [0, 1, 2, 3, 4, 5]

    original = individual.copy()

    rng = random.Random(42)

    swap_mutation(
        individual,
        rng,
    )

    assert individual == original


def test_same_seed_produces_same_mutation():
    individual = [0, 1, 2, 3, 4, 5]

    rng_1 = random.Random(42)
    rng_2 = random.Random(42)

    mutated_1 = swap_mutation(
        individual,
        rng_1,
    )

    mutated_2 = swap_mutation(
        individual,
        rng_2,
    )

    assert mutated_1 == mutated_2


def test_invalid_individual_length():
    individual = [0]

    rng = random.Random(42)

    with pytest.raises(ValueError):
        swap_mutation(
            individual,
            rng,
        )