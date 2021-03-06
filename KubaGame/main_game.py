import pygame
from kuba import Kuba
from constants import SQUARE_SIZE, WIDTH, HEIGHT

if __name__ == '__main__':
    FPS = 60

    KUBA_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Kuba')

    
    def get_row_col_from_mouse(pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col


    def main():
        run = True
        clock = pygame.time.Clock()
        kuba = Kuba(KUBA_WINDOW)

        while run:
            clock.tick(FPS)

            if kuba.get_winner():
                print(f'Winner: {kuba.get_winner()}')
                run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    kuba.select(row, col, KUBA_WINDOW)
            kuba.update_kuba_window()


    main()
