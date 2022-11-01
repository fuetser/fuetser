import random as r
import typing as tp
from copy import deepcopy

import pygame

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

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.rows = self.height // self.cell_size
        self.cols = self.width // self.cell_size

        self.speed = speed
        self.grid = [[]]

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((255, 255, 255))

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        if not randomize:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        return [[r.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell, grid: Cells = None) -> Cells:
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
        new_grid = deepcopy(grid or self.grid)
        for row in range(self.rows):
            for col in range(self.cols):
                neighbours_count = sum(self.get_neighbours((row, col)))
                if neighbours_count == 3:
                    new_grid[row][col] = 1
                elif neighbours_count != 2:
                    new_grid[row][col] = 0
        return new_grid
