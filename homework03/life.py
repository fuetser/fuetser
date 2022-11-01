import pathlib
import random as r
import typing as tp
from copy import deepcopy

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: float = float("inf"),
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

    def create_grid(self, randomize: bool = False) -> Grid:
        if not randomize:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        return [[r.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_row = row + dx
                new_col = col + dy
                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    if new_row != row or new_col != col:
                        neighbours.append(self.curr_generation[new_row][new_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = deepcopy(self.curr_generation)
        for row in range(self.rows):
            for col in range(self.cols):
                neighbours_count = sum(self.get_neighbours((row, col)))
                if neighbours_count == 3:
                    new_grid[row][col] = 1
                elif neighbours_count != 2:
                    new_grid[row][col] = 0
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    def update(self, rows: int, cols: int, max_gen: int = 50, grid=None) -> None:
        self.rows = rows
        self.cols = cols
        self.max_generation = max_gen
        self.curr_generation = grid if grid else self.create_grid(randomize=True)

    def is_cell_alive(self, row: int, col: int) -> bool:
        return bool(self.curr_generation[row][col])

    def switch_cell_status(self, row: int, col: int) -> None:
        self.curr_generation[row][col] = (self.curr_generation[row][col] + 1) % 2

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
            grid = [list(map(int, line)) for line in fi]
        life = GameOfLife((10, 10))
        life.update(len(grid), len(grid[0]), grid=grid)
        return life

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="u8") as fo:
            for row in self.curr_generation:
                print(*row, sep="", file=fo)
