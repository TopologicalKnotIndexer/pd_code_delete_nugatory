"""Detect and remove Reidemeister-I and nugatory PD-code crossings."""

from collections import Counter
from copy import deepcopy
from typing import Hashable


def validate_pd_code(pd_code: object) -> list[list[int]]:
    """Return a normalized copy after weak structural validation."""

    if not isinstance(pd_code, list):
        raise TypeError("PD code must be a list of crossings")
    result: list[list[int]] = []
    for index, crossing in enumerate(pd_code):
        if not isinstance(crossing, (list, tuple)) or len(crossing) != 4:
            raise ValueError(f"crossing {index} must contain exactly four labels")
        normalized: list[int] = []
        for label in crossing:
            if isinstance(label, bool) or not isinstance(label, int) or label <= 0:
                raise ValueError("arc labels must be positive integers")
            normalized.append(label)
        result.append(normalized)

    counts = Counter(label for crossing in result for label in crossing)
    invalid = sorted(label for label, count in counts.items() if count != 2)
    if invalid:
        raise ValueError(f"every arc label must occur exactly twice: {invalid}")
    return result


def _connect(graph: dict[Hashable, set[Hashable]], left: Hashable, right: Hashable):
    graph.setdefault(left, set()).add(right)
    graph.setdefault(right, set()).add(left)


def graph_cc_cnt(pd_code: list[list[int]]) -> int:
    """Count components of the crossing/arc incidence graph."""

    graph: dict[Hashable, set[Hashable]] = {}
    for index, crossing in enumerate(pd_code):
        crossing_node = ("crossing", index)
        graph.setdefault(crossing_node, set())
        for label in crossing:
            _connect(graph, crossing_node, ("arc", label))

    visited: set[Hashable] = set()
    components = 0
    for start in graph:
        if start in visited:
            continue
        components += 1
        visited.add(start)
        stack = [start]
        while stack:
            for neighbor in graph[stack.pop()]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
    return components


def renumber(pd_code: list[list[int]]) -> list[list[int]]:
    """Renumber arcs consecutively while following each link component."""

    current = validate_pd_code(pd_code)
    if not current:
        return []

    adjacency: dict[int, list[int]] = {
        label: [] for crossing in current for label in crossing
    }

    def add_strand(left: int, right: int):
        adjacency[left].append(right)
        adjacency[right].append(left)

    for first, second, third, fourth in current:
        add_strand(first, third)
        add_strand(second, fourth)
    if any(len(neighbors) != 2 for neighbors in adjacency.values()):
        raise ValueError("arc labels do not form closed link components")

    mapping: dict[int, int] = {}
    next_number = 1
    for start in sorted(adjacency):
        if start in mapping:
            continue
        previous: int | None = None
        current_label = start
        while current_label not in mapping:
            mapping[current_label] = next_number
            next_number += 1
            neighbors = list(adjacency[current_label])
            if previous is None:
                following = min(neighbors)
            else:
                try:
                    neighbors.remove(previous)
                except ValueError as exc:
                    raise ValueError("broken strand adjacency") from exc
                following = neighbors[0]
            previous, current_label = current_label, following
        if current_label != start:
            raise ValueError("strand traversal entered a different component")

    return [[mapping[label] for label in crossing] for crossing in current]


def _remove_reidemeister_one(pd_code: list[list[int]]) -> list[list[int]]:
    """Remove all repeated-label crossings before cut-vertex analysis."""

    current = validate_pd_code(deepcopy(pd_code))
    while True:
        index = next(
            (i for i, crossing in enumerate(current) if len(set(crossing)) < 4),
            None,
        )
        if index is None:
            return renumber(current)

        crossing = current[index]
        survivors = [label for label in crossing if crossing.count(label) == 1]
        if len(survivors) not in {0, 2}:
            raise ValueError("unsupported repeated-label crossing")
        current = current[:index] + current[index + 1 :]
        if survivors:
            removed, retained = survivors
            current = [
                [retained if label == removed else label for label in item]
                for item in current
            ]


def is_nugatory(pd_code: list[list[int]], idx: int) -> bool:
    """Return whether crossing `idx` is a cut vertex of the projection graph."""

    current = validate_pd_code(pd_code)
    if not 0 <= idx < len(current):
        raise IndexError(idx)
    if len(set(current[idx])) != 4:
        return False
    without_crossing = current[:idx] + current[idx + 1 :]
    return graph_cc_cnt(without_crossing) > graph_cc_cnt(current)


def get_index_of_nugatory(pd_code: list[list[int]]) -> int | None:
    """Return the first nugatory-crossing index, or `None`."""

    current = validate_pd_code(pd_code)
    for index in range(len(current)):
        if is_nugatory(current, index):
            return index
    return None


def erase_one_nugatory(pd_code: list[list[int]], index: int) -> list[list[int]]:
    """Erase one verified nugatory crossing and reconnect opposite strands."""

    current = validate_pd_code(pd_code)
    if not is_nugatory(current, index):
        raise ValueError(f"crossing {index} is not nugatory")
    first, second, third, fourth = current[index]
    reduced = current[:index] + current[index + 1 :]
    reduced = [
        [third if label == first else label for label in crossing]
        for crossing in reduced
    ]
    reduced = [
        [second if label == fourth else label for label in crossing]
        for crossing in reduced
    ]
    return _remove_reidemeister_one(reduced)


def erase_all_nugatory(pd_code: list[list[int]]) -> list[list[int]]:
    """Remove R1 and nugatory crossings repeatedly to a fixed point."""

    current = _remove_reidemeister_one(pd_code)
    while (index := get_index_of_nugatory(current)) is not None:
        current = erase_one_nugatory(current, index)
    return current
