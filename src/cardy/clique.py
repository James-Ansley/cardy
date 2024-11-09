from collections.abc import Collection
from random import Random

from .distance import distance
from .neighbourhood import neighbourhood
from .types import CardSort, CliqueHeuristic

__all__ = ("Selector", "random_strategy", "greedy_strategy", "clique")


class Selector:
    def __init__(self, seed=None):
        self.random = Random(seed)

    def select[T](self, collection: Collection[T]) -> T:
        """Selects an item from the given collection at random"""
        return self.random.sample(tuple(collection), k=1)[0]


def random_strategy[T](
      _: int,
      candidates: Collection[CardSort[T]],
      selector: Selector = Selector(),
) -> CardSort[T]:
    """
    A heuristic strategy to select clique candidates at random.

    :param _: The max distance between any two sorts in the clique
    :param candidates: The intersection of the current clique
        sort neighbourhoods
    :param selector: An object to select an item from a collection at random
    :return: A randomly selected element
    """
    return selector.select(candidates)


def greedy_strategy[T](
      d: int,
      candidates: Collection[CardSort[T]],
      selector: Selector = Selector(),
) -> CardSort[T]:
    """
    A heuristic strategy to select candidates from a set of sorts to add to a
    clique. See: <https://doi.org/10.1111/j.1468-0394.2005.00304.x>

    In the case where two or more candidates reduce the candidate pool by the
    same amount, one is chosen at random using the given selector.

    :param d: The max distance between any two sorts in the clique
    :param candidates: The intersection of the current clique
        sort neighbourhoods
    :param selector: An object to select an item from a collection at random
    :return: An element that reduces the clique size by the smallest amount
    """
    current_max = 0
    max_candidates = []
    for candidate in candidates:
        size = len(neighbourhood(d, candidate, candidates))
        if size > current_max:
            max_candidates = [candidate]
        elif size == current_max:
            max_candidates.append(candidate)
    return selector.select(max_candidates)


def clique[T](
      d: int,
      probe: CardSort[T],
      sorts: Collection[CardSort[T]],
      strategy: CliqueHeuristic[T] = greedy_strategy,
) -> tuple[CardSort[T], ...]:
    """
    Computes the d-clique centred around the given probe sort using the given
    heuristic strategy.

    The card sorts collection does not need to contain the probe sort. The probe
    sort will not be included in the result in this case.

    The strategy is a heuristic used to select candidate card sorts to add to
    the clique. See <https://doi.org/10.1111/j.1468-0394.2005.00304.x> for more.

    :param d: The max distance between any two sorts in the clique
    :param probe: The starting probe sort
    :param sorts: The collection of card sorts to search for the clique in
    :param strategy: The heuristic strategy for selecting candidates to add to
        the clique.
    :return: A d-clique around the probe sort
    """
    clique_list = [probe] if probe in sorts else []
    candidates = {s for s in sorts if s != probe and distance(s, probe) <= d}
    while candidates:
        selected = strategy(d, candidates)
        clique_list.append(selected)
        candidates = {
            s for s in candidates
            if s != selected and distance(s, selected) <= d
        }
    return tuple(clique_list)