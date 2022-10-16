import random
import sys

import pygame

from src import colors
from src.utils import cur_time
from src.algorithms import IAutomatonAlgorithm


class AliveCell:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    @property
    def key(self):
        return self.x, self.y

    def __repr__(self):
        return f'AliveCell({self.x}, {self.y})'

    def __str__(self):
        return f'AliveCell({self.x}, {self.y})'


class Automaton:
    _screen = None
    _next_fps_tick = 0
    _automaton_algorithm = None
    _algorithm_started = False

    def __init__(self, screen_size=None, cell_count=100, max_fps=60):
        self._screen_size = screen_size or [1280, 720]
        self._screen_ratio = self._screen_size[0] / self._screen_size[1]
        self._max_fps = max_fps
        self._fps_cooldown = 1 / max_fps * 1000

        self._cell_count = cell_count
        self._cell_limits = self._calculate_dimension_limits()
        self._cell_sizes = self._calculate_cell_sizes()
        self._map = {}

    def _calculate_cell_sizes(self):
        width = int(self._screen_size[0] / self._cell_limits[0])
        height = int(self._screen_size[1] / self._cell_limits[1])
        return max(width, 1), max(height, 1)

    def _calculate_dimension_limits(self):
        """
        y*ratio + height = cell_count ---> y = cell_count / (ratio + 1)
        """
        y_cells_count = int(self._cell_count / (self._screen_ratio + 1))
        x_cells_count = self._cell_count - y_cells_count
        return x_cells_count, y_cells_count

    def init_pygame(self):
        pygame.init()
        self._screen = pygame.display.set_mode(self._screen_size)

    def set_algorithm(self, algorithm: IAutomatonAlgorithm):
        self._automaton_algorithm = algorithm

    def start(self):
        while True:
            self._cpu_tick()
            if cur_time() <= self._next_fps_tick:
                continue
            self._next_fps_tick = cur_time() + self._fps_cooldown
            self._fps_tick()

    def _cpu_tick(self):
        self._handle_exit_event()
        self._handle_keyboard()
        self._handle_mouse()

    def _fps_tick(self):
        self._screen.fill(colors.BLACK)
        if self._automaton_algorithm and self._algorithm_started:
            self._automaton_algorithm.automata_tick(self)
        self._draw_alive_cells()
        pygame.display.flip()

    def _handle_exit_event(self):
        quit_events = pygame.event.get(eventtype=pygame.QUIT)
        if len(quit_events) > 0:
            sys.exit()

    def _handle_keyboard(self):
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self._algorithm_started = not self._algorithm_started

    def _handle_mouse(self):
        mouse_events = [
            *pygame.event.get(eventtype=pygame.MOUSEMOTION),
            *pygame.event.get(eventtype=pygame.MOUSEBUTTONDOWN),
        ]
        if len(mouse_events) == 0:
            return
        add, _, remove = pygame.mouse.get_pressed(num_buttons=3)
        if not any([add, remove]):
            return

        pos = pygame.mouse.get_pos()
        cell_x, cell_y = int(pos[0] / self._cell_sizes[0]), int(pos[1] / self._cell_sizes[1])

        if add:
            self._alive_cell(cell_x, cell_y)
        elif remove:
            self._kill_cell(cell_x, cell_y)

    def _get_cell(self, x, y):
        return self._map.get((x, y))

    def _set_cell(self, x, y, cell):
        key = (x, y)
        if not cell:
            del self._map[key]
        else:
            self._map[key] = cell

    def _is_alive(self, x, y):
        return self._get_cell(x, y)

    def _in_limits(self, x, y):
        return (
            0 <= x < self._cell_limits[0] and
            0 <= y < self._cell_limits[1]
        )

    def _alive_cell(self, x, y):
        if self._is_alive(x, y) or not self._in_limits(x, y):
            return

        color = colors.RANDOM_NEAR(colors.AZURE)
        alive_cell = AliveCell(x, y, color)
        self._set_cell(x, y, alive_cell)

    def _kill_cell(self, x, y):
        if not self._is_alive(x, y) or not self._in_limits(x, y):
            return

        self._set_cell(x, y, None)

    def _draw_alive_cells(self):
        for cell in self._map.values():
            self._draw_cell(cell)

    def _draw_cell(self, cell: AliveCell):
        start = cell.x * self._cell_sizes[0], cell.y * self._cell_sizes[1]
        pygame.draw.rect(self._screen, cell.color, pygame.Rect(*start, self._cell_sizes[0], self._cell_sizes[1]))


