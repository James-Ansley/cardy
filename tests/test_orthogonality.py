from pytest import approx

from cardy import orthogonality
from cardy.orthogonality import DisjointSet, min_spanning_tree
from utils import test

# TODO — Test this properly. These are just ad hoc test cases.


@test
def disjoint_sets():
    forest = DisjointSet(range(1, 11))
    for i in range(1, 11):
        assert forest.find(i) == i
    forest.merge(1, 2)
    forest.merge(2, 3)
    forest.merge(3, 3)
    forest.merge(3, 4)
    root = forest.find(1)
    forest.merge(5, 6)
    forest.merge(6, 4)
    assert forest.find(6) == root


@test
def spanning_trees():
    vertices = ["A", "B", "C", "D", "E", "F", "G"]
    edges = {
        ('A', 'B'): 7,
        ('A', 'D'): 5,
        ('B', 'C'): 8,
        ('B', 'D'): 9,
        ('B', 'E'): 7,
        ('C', 'E'): 5,
        ('D', 'E'): 15,
        ('D', 'F'): 6,
        ('E', 'F'): 8,
        ('E', 'G'): 9,
        ('F', 'G'): 11,
    }
    assert min_spanning_tree(vertices, edges) == {
        ('E', 'G'), ('A', 'B'), ('D', 'F'), ('C', 'E'), ('B', 'E'), ('A', 'D')
    }


@test
def nmst_metric():
    # Examples from: https://doi.org/10.1111/j.1468-0394.2005.00305.x
    a = (
        ({1, 3, 4, 5, 6, 7, 13, 14, 15, 22, 23},
         {2, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20, 21, 24, 25, 26}),
        ({1, 3, 4, 6, 7, 10, 13, 14, 15, 18, 23, 26},
         {2, 5, 8, 9, 11, 12, 16, 17, 19, 20, 21, 22, 24, 25}),
        ({1, 2, 5, 8, 9, 11, 12, 16, 17, 18, 19, 20, 21, 22, 24, 25},
         {3, 4, 6, 7, 10, 13, 14, 15, 23, 26}),
    )
    b = (
        ({9, 17, 18, 25},
         {1, 3, 5, 8, 12, 13, 20, 26},
         {2, 6, 7, 10, 11, 15, 19, 22},
         {4, 14, 16, 21, 23},
         {24}),
        ({12, 20},
         {18, 25},
         {3, 13, 19},
         {5, 10, 15},
         {1, 17},
         {8, 9},
         {2, 4, 6, 7, 11, 14, 16, 21, 22, 23, 24, 26}),
        ({1, 3, 5, 6, 7, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20, 21, 25, 26},
         {2, 4, 8, 13, 17, 22, 23, 24})
    )
    assert orthogonality(a) == approx(7 / 3)  # 2.33...
    assert orthogonality(b) == approx(11.0)
