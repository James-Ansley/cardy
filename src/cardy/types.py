from collections.abc import Callable, Collection, Hashable, Set

__all__ = ("CardSort", "CliqueHeuristic")

type CardSort[T: Hashable] = Collection[Set[T]]
type CliqueHeuristic[T] = Callable[[int, Collection[CardSort[T]]], CardSort[T]]
