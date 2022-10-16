from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.automaton import Automaton


class IAutomatonAlgorithm(ABC):
    @abstractmethod
    def automata_tick(self, automaton: 'Automaton'):
        pass


class LifeGame(IAutomatonAlgorithm):
    _a = None
    _neighbours_vectors = (
        (-1, 0),
        (-1, -1),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, 0),
        (1, -1),
        (1, 1),
    )

    def _should_be_alive(self, x, y):
        alive_neighbours_count = 0
        is_alive = self._a._is_alive(x, y)
        for vector in self._neighbours_vectors:
            if self._a._is_alive(x + vector[0], y + vector[1]):
                alive_neighbours_count += 1

        if is_alive:
            return self._should_stay_alive(alive_neighbours_count)
        return self._should_became_alive(alive_neighbours_count)

    def _should_stay_alive(self, alive_neighbours_count):
        return alive_neighbours_count in [2, 3]

    def _should_became_alive(self, alive_neighbours_count):
        return alive_neighbours_count == 3

    def _populate_cells_to_check(self):
        to_check = {}
        for cell in self._a._map.keys():
            to_check[cell] = True
            self._populate_cell_neighbours(to_check, cell)
        return to_check

    def _populate_cell_neighbours(self, to_check, cell):
        for vector in self._neighbours_vectors:
            neighbour = cell[0] + vector[0], cell[1] + vector[1]
            if to_check.get(neighbour) or not self._a._in_limits(*neighbour):
                continue
            to_check[neighbour] = True

    def _apply_results(self, results):
        for cell, is_alive in results.items():
            if is_alive:
                self._a._alive_cell(*cell)
            else:
                self._a._kill_cell(*cell)

    def automata_tick(self, automaton: 'Automaton'):
        self._a = automaton
        results = {}

        to_check = self._populate_cells_to_check()
        for cell in to_check.keys():
            results[cell] = self._should_be_alive(*cell)

        self._apply_results(results)


class LifeGameWithoutDeath(LifeGame):
    def _should_stay_alive(self, alive_neighbours_count):
        return alive_neighbours_count >= 4

    def _should_became_alive(self, alive_neighbours_count):
        return alive_neighbours_count >= 5


class LifeGameWithoutDeath2(LifeGame):
    def _should_stay_alive(self, alive_neighbours_count):
        return True

    def _should_became_alive(self, alive_neighbours_count):
        return alive_neighbours_count == 1
