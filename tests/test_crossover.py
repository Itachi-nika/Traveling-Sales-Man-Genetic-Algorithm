import random

import pytest

from src.crossover import order_crossover


def test_children_are_valid_permutations():
    parent_1 = [0, 1, 2, 3, 4, 5, 6, 7]
    parent_2 = [3, 7, 5, 1, 6, 0, 2, 4]

    rng = random.Random(42)

    child_1, child_2 = order_crossover(
        parent_1,
        parent_2,
        rng,
    )

    expected = list(range(8))

    assert sorted(child_1) == expected
    assert sorted(child_2) == expected


def test_children_have_correct_length():
    parent_1 = [0, 1, 2, 3, 4]
    parent_2 = [4, 3, 2, 1, 0]

    rng = random.Random(42)

    child_1, child_2 = order_crossover(
        parent_1,
        parent_2,
        rng,
    )

    assert len(child_1) == 5
    assert len(child_2) == 5


def test_crossover_does_not_modify_parents():
    parent_1 = [0, 1, 2, 3, 4]
    parent_2 = [4, 3, 2, 1, 0]

    original_parent_1 = parent_1.copy()
    original_parent_2 = parent_2.copy()

    rng = random.Random(42)

    order_crossover(
        parent_1,
        parent_2,
        rng,
    )

    assert parent_1 == original_parent_1
    assert parent_2 == original_parent_2


def test_same_seed_produces_same_children():
    parent_1 = [0, 1, 2, 3, 4, 5]
    parent_2 = [5, 4, 3, 2, 1, 0]

    rng_1 = random.Random(42)
    rng_2 = random.Random(42)

    children_1 = order_crossover(
        parent_1,
        parent_2,
        rng_1,
    )

    children_2 = order_crossover(
        parent_1,
        parent_2,
        rng_2,
    )

    assert children_1 == children_2


def test_different_parent_lengths_raise_error():
    parent_1 = [0, 1, 2, 3]
    parent_2 = [0, 1, 2]

    rng = random.Random(42)

    with pytest.raises(ValueError):
        order_crossover(
            parent_1,
            parent_2,
            rng,
        )


def test_parents_with_different_cities_raise_error():
    parent_1 = [0, 1, 2, 3]
    parent_2 = [0, 1, 2, 4]

    rng = random.Random(42)

    with pytest.raises(ValueError):
        order_crossover(
            parent_1,
            parent_2,
            rng,
        )