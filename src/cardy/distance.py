# Copyright 2025 Cardy Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from munkres import Munkres, make_cost_matrix

from .types import CardSort

__all__ = ("distance",)


def distance[T](sort1: CardSort[T], sort2: CardSort[T]) -> int:
    """Computes the edit distance between the two given card sorts."""
    if not sort1 and not sort2:
        return 0

    weights = [
        [len(group1 & group2) for group2 in sort2]
        for group1 in sort1
    ]
    cost_matrix = make_cost_matrix(weights)
    total = sum([
        weights[row][col]
        for row, col in Munkres().compute(cost_matrix)
    ])
    return sum(len(g) for g in sort1) - total
