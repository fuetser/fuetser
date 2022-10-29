import argparse
import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.from_cmd_args()

    def draw(self, screen) -> None:
        screen.addstr(f"+{'-' * self.life.cols}+\n")
        for row in self.life.curr_generation:
            screen.addch("|")
            for el in row:
                screen.addch("*" if el else " ")
            screen.addstr("|\n")
        screen.addstr(f"+{'-' * self.life.cols}+\n")

    def run(self) -> None:
        screen = curses.initscr()
        while True:
            screen.clear()
            self.draw(screen)
            screen.refresh()
            self.life.step()
            time.sleep(0.2)
        curses.endwin()

    def from_cmd_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--rows", type=int)
        parser.add_argument("--cols", type=int)
        parser.add_argument("--max-generations", type=int)
        args = parser.parse_args()
        if args.rows and args.cols and args.max_generations:
            self.life.update(args.rows, args.cols, args.max_generations)


if __name__ == "__main__":
    life = GameOfLife((24, 80), max_generations=50)
    c = Console(life)
    c.run()
