import json
from typing import Collection

from cardy import clique
from cardy.clique import Selector, greedy_strategy
from utils import test


def load_examples():
    with open("examples.json", "r") as f:
        data = json.load(f)
    return {k: tuple(set(c) for c in v.values()) for k, v in data.items()}


class MinSelector(Selector):
    def select[T](self, collection: Collection[T]) -> T:
        return min(collection)


class MaxSelector(Selector):
    def select[T](self, collection: Collection[T]) -> T:
        return max(collection)


@test
def a_clique_of_equivalent_sorts_returns_the_whole_set_of_sort_ids():
    assert clique(0, ({1}, {2}), {0: ({1}, {2}), 1: ({2}, {1})}) == {0, 1}
    assert clique(1, ({1}, {2}), {0: ({1}, {2}), 1: ({2}, {1})}) == {0, 1}


@test
def cliques_do_not_necessarily_contain_the_probe_sort():
    assert clique(0, ({1, 2},), {0: ({1}, {2}), 1: ({2}, {1})}) == set()
    assert clique(1, ({1, 2},), {0: ({1}, {2}), 1: ({2}, {1})}) == {0, 1}


@test
def cliques_exclude_items_even_if_they_are_in_the_neighbourhood_of_the_card_sort():
    sorts = {
        0: ({1}, {2}, {3}),
        1: ({2, 3}, {1}),
        2: ({1, 2, 3},),
    }
    assert clique(
        1, ({1, 2}, {3}), sorts,
        strategy=lambda d, c: greedy_strategy(d, c, MinSelector())
    ) == {0, 1}
    assert clique(
        1, ({1, 2}, {3}), sorts,
        strategy=lambda d, c: greedy_strategy(d, c, MaxSelector())
    ) == {1, 2}


@test
def example_cliques():
    """
    Examples taken from: https://doi.org/10.1111/j.1468-0394.2005.00304.x
    """
    sorts = load_examples()
    # Table 5 Deibel et al.
    assert clique(4, sorts["table-5-0/8-4"], sorts) == {
        "table-5-0/8-4", "table-5-1", "table-5-2", "table-5-3", "table-5-4",
        "table-5-5", "table-5-6", "table-5-7", "table-5-8", "table-5-9/8-5",
    }
    # Table 6 Deibel et al.
    assert clique(
        5,
        sorts["table-6-0"],
        sorts,
        strategy=lambda d, c: greedy_strategy(d, c, MinSelector()),
    ) == {
        "table-6-0", "table-6-1", "table-6-2", "table-6-3",
        "table-6-4", "table-6-5", "table-6-6", "table-6-7",
    }
    # Table 7 Deibel et al.
    assert clique(5, sorts["table-7-0"], sorts) == {
        "table-7-0", "table-7-1", "table-7-2",
        "table-7-3", "table-7-4", "table-7-5",
    }
    # Table 8 Deibel et al.
    assert clique(
        5,
        sorts["table-8-0"],
        sorts,
        strategy=lambda d, c: greedy_strategy(d, c, MaxSelector()),
    ) == {
        "table-8-0", "table-8-1", "table-8-2", "table-8-3",
        "table-5-0/8-4", "table-5-9/8-5",
    }
