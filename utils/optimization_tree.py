"""
Module to handle optimization problems
"""
from typing import *
from abc import ABC, abstractmethod

T = TypeVar('T')


class OptimizationTree(ABC, Generic[T]):
    def __init__(self, start_val: T):
        self._children_map: Dict[T, Optional[List[T]]] = {start_val: None}
        self._layers = [{start_val}]
        self._scores = {start_val: self.evaluate(start_val, 0)}

    @abstractmethod
    def find_children(self, parent: T, layer: int) -> List[T]:
        pass

    def evaluate(self, state: T, layer: int) -> Union[float, int]:
        return state

    def trim_leaf(self, leaf: T, layers: List[Set[T]], leaf_layer: int) -> bool:
        return False

    def add_layer(self):
        self._layers.append(set())
        for leaf in self._layers[-2]:
            if self.trim_leaf(leaf, self._layers, len(self._layers) - 2):
                continue
            children = self.find_children(leaf, len(self._layers) - 1)
            self._children_map[leaf] = children
            for child in children:
                if child in self._children_map:
                    continue
                self._children_map[child] = None
                self._scores[child] = self.evaluate(child, len(self._layers) - 1)
            self._layers[-1].update(children)

    def run(self, num_layers: int):
        for _ in range(num_layers):
            self.add_layer()

    def best_result(self, require_leaf: bool = True) -> Tuple[T, Union[float, int]]:
        best = None
        for state, children in self._children_map.items():
            if require_leaf and children is not None:
                continue
            score = self._scores[state]
            if best is None or score > best[1]:
                best = state, score
        return best
