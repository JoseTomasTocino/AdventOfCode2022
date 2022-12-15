import pygame


class Viz:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((900, 900))
        self.rect = pygame.Rect(self.window.get_rect().center, (900, 900))

    def set(self, x, y, color):
        margin_x = 50
        margin_y = 50

        pixel_size = 2
        for i in range(pixel_size):
            for j in range(pixel_size):
                self.window.set_at(
                    (margin_x + x * pixel_size + i, margin_y + y * pixel_size + j), color
                )
        pygame.display.flip()
        # pygame.time.wait(1)

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.flip()

        pygame.quit()
