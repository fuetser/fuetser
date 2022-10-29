import pathlib
import random
import typing as tp

import pygame
from life_proto import GameOfLife as GameOfLifeProto
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife(GameOfLifeProto):
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def get_neighbours(self, cell: Cell) -> Cells:
        return super().get_neighbours(cell, self.curr_generation)

    def get_next_generation(self) -> Grid:
        return super().get_next_generation(self.curr_generation)

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    def update(self, rows: int, cols: int, max_gen: int) -> None:
        self.rows = rows
        self.cols = cols
        self.max_generation = max_gen
        self.curr_generation = self.create_grid(randomize=True)

    def is_cell_alive(self, row: int, col: int) -> bool:
        return bool(self.curr_generation[row][col])

    def switch_cell_status(self, row: int, col: int) -> None:
        self.curr_generation[row][col] = (
            self.curr_generation[row][col] + 1) % 2

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, encoding="u8") as fi:
            self.current_generation = [list(map(int, line)) for line in fi]

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="u8") as fo:
            for row in self.current_generation:
                print(*row, sep="", file=fo)
