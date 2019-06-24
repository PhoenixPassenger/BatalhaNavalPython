import pygame
from threading import Thread
def pygameStart():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0,0,255)

    WIDTH = 20
    HEIGHT = 20

    MARGIN = 5
    MARGIN_TABLE = 10.5
    grid = []

    columns = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']

    for row in range(14):
        grid.append([])
        for column in range(14):
            grid[row].append(0)

    pygame.init()

    WINDOW_SIZE = [350, 350]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("NAVAL BATTLE")

    done = False

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                if grid[row][column] > 3:
                    grid[row][column] = 0
                grid[row][column] += 1
                print("Click ", pos, "Grid coordinates: ", row + 1, columns[column])


        screen.fill(BLACK)

        for row in range(14):
            for column in range(14):
                color = WHITE
                if grid[row][column] == 1:
                    color = GREEN
                elif grid[row][column] == 2:
                    color = BLUE
                elif grid[row][column] == 3:
                    color = RED
                elif grid[row][column] == 0:
                    color = WHITE
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()

pygameStart()