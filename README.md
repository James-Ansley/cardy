# Cardy

[![Repository](https://img.shields.io/badge/james--ansley%2Fcardypy-102335?logo=codeberg&labelColor=07121A)](https://codeberg.org/james-ansley/cardypy)
[![License](https://img.shields.io/badge/Apache--2.0-green?label=license)](https://codeberg.org/james-ansley/cardypy/src/branch/main/LICENSE)
[![PyPi](https://img.shields.io/pypi/v/cardy?label=PyPi&labelColor=%23ffd343&color=%230073b7)](https://pypi.org/project/cardy/)

Low-level card sorting utilities to compare card sorts — including calculating
edit distances, d-neighbourhoods, d-cliques, and orthogonality of card sorts.

It is recommended to read
[Deibel et al. (2005)](https://doi.org/10.1111/j.1468-0394.2005.00304.x)[^1]
and [Fossum & Haller (2005)](https://doi.org/10.1111/j.1468-0394.2005.00305.x)[^2]
to familiarize yourself with the metrics covered in this library. In fact, that
entire special issue of Expert Systems is excellent reading for anyone
interested in analysing card sorting data.

## Installation

```bash
pip install cardy
```

## Usage

Card sorts are represented as collections of sets of cards: `Colection[Set[T]]`
where each set represents a group.

### Edit Distance

The edit distance between two sorts can be computed with the distance function:

```python
from cardy import distance

sort1 = ({1, 2, 3}, {4, 5, 6}, {7, 8, 9})
sort2 = ({1, 2}, {3, 4}, {5, 6, 7}, {8, 9})

dist = distance(sort1, sort2)
print("Distance:", dist)  # Distance: 3
```

When comparing sorts for equality, assert an edit distance of zero:

```python
if distance(sort1, sort2) == 0:
    ...
```

#### Maximum and Normalised Edit Distances

Normalised edit distances can be computed with the norm_distance function:

```python
from cardy import norm_distance

sort1 = (
    {"a1", "a2", "a3"},
    {"b1", "b2", "b3", "b4", "b5"},
    {"c1", "c2", "c3", "c4", "c5"},
    {"d1", "d2", "d3", "d4"},
)
sort2 = (
    {"a1", "b1", "b5", "c1", "c5", "d1"},
    {"a2", "b2", "c2", "d2"},
    {"a3", "b3", "c3", "d3"},
    {"b4", "c4", "d4"},
)

print(norm_distance(sort1, sort2))  # 0.92...
print(norm_distance(sort1, sort2, num_groups=4))  # 1.0
```

The `num_groups` option specifies the normalised distance should be computed
under the assumption the maximum number of groups in either card sort will not
exceed `num_groups`. If this option is not given, distances are normalised with
no limit on the number of groups.

The maximum edit distance any other card sort can be from a given card sort can
be computed with the maxDistance function.

```python
from cardy import max_distance

# Using sort1 from the previous example
print(max_distance(sort1))  # 13
print(max_distance(sort1, num_groups=4))  # 12
```

As before, the `num_groups` option places a restriction on the maximum number of
groups another card sort may have.

### Cliques and Neighbourhoods

Cliques and neighbourhoods can be calculated using the `clique`
and `neighbourhood` functions. Given a mapping of sort IDs to card sorts:
`Mapping[K, Collection[Set[T]]]`, a neighbourhood or clique is represented as a
set of IDs: `Set[K]` of card sorts

#### Neighbourhoods

Neighbourhoods are always deterministic:

```python
from cardy import neighbourhood

probe = ({1, 2, 3, 4, 5},)
sorts = {
    0: ({1, 2, 3}, {4, 5}),
    1: ({1, 2, 3}, {4, 5}, set()),
    2: ({1, 2}, {3}, {4, 5}),
    3: ({1, 2}, {3, 4}, {5}),
    4: ({1, 2, 4}, {3, 5}),
}

two_neighbourhood = neighbourhood(2, probe, sorts)
print(f"2-neighbourhood around `{probe}`: {two_neighbourhood}")
# 2-neighbourhood around `({1, 2, 3, 4, 5},)`: {0, 1, 4}
```

Neighbourhoods can be calculated using normalised edit distances by passing a
custom edit distance function as a named argument:

```python
dist = lambda l, r: norm_distance(l, r, num_groups=3)
upper_quart_neighbourhood = neighbourhood(0.75, probe, sorts, distance=dist)
print(f"Sorts within 75% of `{probe}` are {upper_quart_neighbourhood}")
# Sorts within 75% of `({1, 2, 3, 4, 5},)` are {0, 1, 4}
```

#### Cliques

Cliques can be non-deterministic — even when using a greedy strategy (default):

```python
from cardy import clique

probe = ({1, 2}, {3})
sorts = {
    0: ({1}, {2}, {3}),
    1: ({2, 3}, {1}),
    2: ({1, 2, 3},),
}
one_clique = clique(1, probe, sorts)
print(f"1-clique around `{probe}`: {one_clique}")
# 1-clique around `({1, 2}, {3})`: {0, 1}
# OR
# 1-clique around `({1, 2}, {3})`: {1, 2}
```

The clique function allows for various heuristic strategies for selecting
candidate card sorts (via ID). Heuristic functions are of the form:
`(int, Mapping[K, Collection[Set[T]]]) -> K` — that is, a function that takes a
the maximum clique diameter and a key to card sort mapping of viable candidates,
and returns a key of a viable candidate based on some heuristic.

Two heuristic functions have been provided: `random_strategy` and
`greedy_strategy`. `random_strategy` will select a candidate at random.
`greedy_strategy` will select a candidate that reduces the size of the candidate
pool by the smallest amount. In the case two or more candidates reduce the pool
by the same amount, one is selected at random.

This behaviour can be changed by providing a deterministic heuristic function,
or a deterministic `Selector` which provides a select method that picks a
candidate in the case of ambiguity:

```python
from cardy import clique
from cardy.clique import Selector, greedy_strategy


class MinSelector(Selector):
    def select(self, collection):
        # selects the candidate with the smallest key in case of ties
        # for greedy strategy
        return min(collection)


probe = ({1, 2}, {3})
sorts = {
    0: ({1}, {2}, {3}),
    1: ({2, 3}, {1}),
    2: ({1, 2, 3},),
}
one_clique = clique(
    1,
    probe,
    sorts,
    strategy=lambda d, c: greedy_strategy(d, c, MinSelector())
)
print(f"1-clique around `{probe}`: {one_clique}")
# 1-clique around `({1, 2}, {3})`: {0, 1}
```

Alternatively, a seed can be passed to the base `Selector` constructor.

As with neighbourhoods, a normalised edit distance function can be passed to the
clique call as an option:

```python
dist = lambda l, r: norm_distance(l, r, num_groups=3)
one_clique = clique(1, probe, sorts, selector=MinSelector(), distance=dist)
print("100%-clique around", probe, "is", oneClique);
# 100%-clique around ({1, 2}, {3}) is {0, 1, 2}
# Not an exciting example.
# But what are ya gonna do? Ya know. Just one of those days.
```

### Orthogonality

The orthogonality of a collection of sorts can be calculated with the
`orthogonality` function:

```python
from cardy import orthogonality

p1 = (
    ({1, 3, 4, 5, 6, 7, 13, 14, 15, 22, 23},
     {2, 8, 9, 10, 11, 12, 16, 17, 18, 19, 20, 21, 24, 25, 26}),
    ({1, 3, 4, 6, 7, 10, 13, 14, 15, 18, 23, 26},
     {2, 5, 8, 9, 11, 12, 16, 17, 19, 20, 21, 22, 24, 25}),
    ({1, 2, 5, 8, 9, 11, 12, 16, 17, 18, 19, 20, 21, 22, 24, 25},
     {3, 4, 6, 7, 10, 13, 14, 15, 23, 26}),
)
p1_orthogonality = orthogonality(p1)
print(f"P1 orthogonality: {p1_orthogonality:.2f}")  # P1 orthogonality: 2.33
```

A custom edit distance function can be passed to the orthogonality calculation:

```python
dist = lambda l, r: norm_distance(l, r, num_groups=2)
p1_orthogonality = orthogonality(p1, distance=dist)
print(f"P1 normalized orthogonality: {p1_orthogonality:.2f}") 
# P1 normalized orthogonality: 0.18
```

[^1]: Deibel, K., Anderson, R. and Anderson, R. (2005), Using edit distance to
analyze card sorts. Expert Systems, 22: 129-138.
https://doi.org/10.1111/j.1468-0394.2005.00304.x

[^2]: Fossum, T. and Haller, S. (2005), Measuring card sort orthogonality.
Expert Systems, 22: 139-146. https://doi.org/10.1111/j.1468-0394.2005.00305.x
