import pathlib
import typing as tp
from random import randint

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """Сгруппировать значения values в список, состоящий из списков по n элементов"""
    res = []
    tmp = []
    for value in values:
        tmp.append(value)
        if len(tmp) == n:
            res.append(tmp)
            tmp = []
    return res


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos"""
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos"""
    return [row[pos[1]] for row in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos"""
    res = []
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            res.append(grid[i][j])
    return res


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле"""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == ".":
                return row, col
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции"""
    row_values = set(get_row(grid, pos)) - {"."}
    col_values = set(get_col(grid, pos)) - {"."}
    block_values = set(get_block(grid, pos)) - {"."}
    return set(map(str, range(1, len(grid) + 1))) - row_values - col_values - block_values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    pos = find_empty_positions(grid)
    if not pos:
        return grid
    else:
        for value in find_possible_values(grid, pos):
            grid[pos[0]][pos[1]] = value
            if solve(grid):
                return grid
            grid[pos[0]][pos[1]] = "."
    return None


def check_solution(grid: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    length = len(grid)
    flag1 = True
    flag2 = True
    flag3 = True
    for i in range(length):
        flag1 = flag1 and len(set(grid[i]) - {"."}) == length
        flag2 = flag2 and len(set(grid[j][i] for j in range(length)) - {"."}) == length
        for j in range(length):
            flag3 = flag3 and len(set(get_block(grid, (i, j))) - {"."}) == length
    return flag1 and flag2 and flag3


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов"""
    grid = [["."] * 9 for _ in range(9)]
    solve(grid)
    for _ in range(81 - N):
        while True:
            row = randint(0, 8)
            col = randint(0, 8)
            if grid[row][col] != ".":
                break
        grid[row][col] = "."
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
