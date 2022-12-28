import pygame

WIN_HEIGHT = 1200

class Viz:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((900, WIN_HEIGHT))
        self.rect = pygame.Rect(self.window.get_rect().center, (900, WIN_HEIGHT))

    def set(self, x, y, color, flip=True):
        margin_x = 20
        margin_y = 20

        # y = WIN_HEIGHT - y

        pixel_size = 30
        for i in range(pixel_size):
            for j in range(pixel_size):
                self.window.set_at(
                    (margin_x + x * pixel_size + i, margin_y + y * pixel_size + j),
                    color,
                )
        if flip:
            pygame.display.flip()
            pygame.time.wait(200)

    def reset(self):
        self.window.fill(0)

    def draw(self, grid, temp_rock=None):
        self.reset()

        highest_point = 0

        # X is a defualtdict with with pairs like {y: bool}
        for x in grid.values():
            for y, v in x.items():
                if v and y > highest_point:
                    highest_point = y
            

        if temp_rock:
            highest_point = max(highest_point, max(p.y for p in temp_rock.elems))

        if highest_point < round(WIN_HEIGHT / 7):
            highest_point = round(WIN_HEIGHT / 7)

        for y in range(highest_point, -1, -1):
            self.set(-1, y, (255, 255, 255))
            self.set(7, y, (255, 255, 255))
            
            for x in range(7):
                if grid[x][y]:
                    self.set(x, highest_point - y, (50, 50, 50))

                if temp_rock and (x,y) in [(p.x, p.y) for p in temp_rock.elems]:
                    self.set(x, highest_point - y, (255, 0, 0))


        pygame.display.flip()
        pygame.time.wait(100)

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.flip()

        pygame.quit()
