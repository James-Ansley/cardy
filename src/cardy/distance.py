from munkres import Munkres, make_cost_matrix

from .types import CardSort

__all__ = ("distance",)


def distance[T](sort1: CardSort[T], sort2: CardSort[T]) -> int:
    """Computes the edit distance between the two given card sorts."""
    if not sort1 and not sort2:
        return 0

    # TODO — Possible optimization. List comprehensions are probably the most
    #  optimized thing in Python. Given sorts are unlikely to contain more
    #  than ~30 cards the space trade off is probably worth it for the
    #  huge constant time improvements.
    #  Will need to test later.
    # weights = [[len(group1 & group2) for group2 in sort2] for group1 in sort1]
    # total = sum([
    #     weights[row][col]
    #     for row, col in Munkres().compute(make_cost_matrix(weights))
    # ])
    # return sum(len(g) for g in sort1) - total

    matching_weights = [[] for _ in range(len(sort1))]
    for i, group1 in enumerate(sort1):
        for group2 in sort2:
            intersection = len(group1 & group2)
            matching_weights[i].append(intersection)

    cost_matrix = make_cost_matrix(matching_weights)

    running_sum = 0
    for row, col in Munkres().compute(cost_matrix):
        running_sum += matching_weights[row][col]

    return sum(len(g) for g in sort1) - running_sum
