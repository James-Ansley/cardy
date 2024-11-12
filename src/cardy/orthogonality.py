from collections.abc import Collection, Mapping
from itertools import combinations

from . import distance
from .types import CardSort

__all__ = ("DisjointSet", "min_spanning_tree", "orthogonality")


class DisjointSet[K]:
    def __init__(self, elements: Collection[K]):
        self.parents = {e: e for e in elements}
        self.sizes = {e: 1 for e in elements}

    def find(self, e: K) -> K:
        root = e
        while self.parents[root] != root:
            root = self.parents[root]
        while self.parents[e] != root:
            parent = self.parents[e]
            self.parents[e] = root
            e = parent
        return root

    def merge(self, e1: K, e2: K) -> None:
        e1 = self.find(e1)
        e2 = self.find(e2)
        if e1 == e2:
            return

        if self.sizes[e1] < self.sizes[e2]:
            e1, e2 = e2, e1
        self.parents[e2] = e1
        self.sizes[e1] += self.sizes[e2]


def min_spanning_tree[K](
      vertices: Collection[K],
      edges: Mapping[tuple[K, K], int]
) -> set[tuple[K, K]]:
    f = set()
    forest = DisjointSet(vertices)
    for (e1, e2), _ in sorted(edges.items(), key=lambda it: it[1]):
        if forest.find(e1) != forest.find(e2):
            f.add((e1, e2))
            forest.merge(e1, e2)
    return f


def orthogonality[T](sorts: Collection[CardSort[T]]) -> float:
    """
    Returns the orthogonality of the given collection of sorts.

    See: https://doi.org/10.1111/j.1468-0394.2005.00305.x
    """
    sorts = {i: s for i, s in enumerate(sorts)}
    edges = {
        (e1, e2): distance(s1, s2)
        for (e1, s1), (e2, s2) in combinations(sorts.items(), 2)
    }
    tree = min_spanning_tree(sorts, edges)
    total_weight = sum(edges[e] for e in tree)
    return total_weight / len(sorts)