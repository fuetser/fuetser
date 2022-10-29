import random as r
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.rows = self.height // self.cell_size
        self.cols = self.width // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if not randomize:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        return [[r.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell, grid: Cells = None) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        grid = grid or self.grid
        row, col = cell
        neighbours = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_row = row + dx
                new_col = col + dy
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    if new_row != row or new_col != col:
                        neighbours.append(grid[new_row][new_col])
        return neighbours

    def get_next_generation(self, grid: Cells = None) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = deepcopy(grid or self.grid)
        for row in range(self.rows):
            for col in range(self.cols):
                neighbours_count = sum(self.get_neighbours((row, col)))
                if neighbours_count == 3:
                    new_grid[row][col] = 1
                elif neighbours_count != 2:
                    new_grid[row][col] = 0
        return new_grid


if __name__ == '__main__':
    life = GameOfLife()
    life.grid = life.create_grid(randomize=True)
    life.run()
