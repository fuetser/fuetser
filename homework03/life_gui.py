import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.border_width = 1
        self.screen_size = (
            self.life.cols * cell_size + self.border_width,
            self.life.rows * cell_size + self.border_width,
        )
        self.display = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.is_paused = False
        pygame.display.set_caption("Game of Life")

    def draw_lines(self, win) -> None:
        # vertical
        for col in range(self.life.cols + 1):
            pygame.draw.line(
                win,
                "black",
                (col * self.cell_size, 0),
                (col * self.cell_size, self.screen_size[1]),
                self.border_width,
            )
        # horizontal
        for row in range(self.life.rows + 1):
            pygame.draw.line(
                win,
                "black",
                (0, row * self.cell_size),
                (self.screen_size[0], row * self.cell_size),
                self.border_width,
            )

    def draw_grid(self, win) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.is_cell_alive(row, col):
                    pygame.draw.rect(
                        win,
                        "green",
                        (
                            col * self.cell_size,
                            row * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

    def process_click(self, pos: tuple[int, int]) -> None:
        col = pos[0] // self.cell_size
        row = pos[1] // self.cell_size
        self.life.switch_cell_status(row, col)

    def redraw(self, win) -> None:
        win.fill("white")
        self.draw_grid(win)
        self.draw_lines(win)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.is_paused = not self.is_paused

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.is_paused:
                    self.process_click(event.pos)

    def run(self) -> None:
        while True:
            self.handle_events()
            self.redraw(self.display)
            if not self.is_paused:
                self.life.step()
            pygame.display.update()
            self.clock.tick(self.speed)


if __name__ == "__main__":
    pygame.init()
    life = GameOfLife((50, 50), max_generations=50)
    gui = GUI(life)
    gui.run()
