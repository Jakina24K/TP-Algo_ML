import pygame
import sys
from logic.puzzle_logic import create_puzzle, move_tile, check_win
from ui.win_screen import show_win_screen
from ui.start_screen import show_start_screen

TILE_SIZE = 100

def draw_grid(screen, puzzle):
    n = len(puzzle)
    font = pygame.font.Font(None, TILE_SIZE // 2)
    for row in range(n):
        for col in range(n):
            value = puzzle[row][col]
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 2)
            if value != 0:
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def game_loop(n):
    puzzle = create_puzzle(n)
    screen = pygame.display.set_mode((n * TILE_SIZE, n * TILE_SIZE + 50))
    pygame.display.set_caption(f"n-Puzzle ({n}x{n})")
    font = pygame.font.Font(None, 36)
    back_button_rect = pygame.Rect(10, n * TILE_SIZE + 10, 100, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button_rect.collidepoint((x, y)):
                    return  # Retourne à l'écran d'accueil
                if y < n * TILE_SIZE:
                    row, col = y // TILE_SIZE, x // TILE_SIZE
                    move_tile(puzzle, row, col)
                    if check_win(puzzle):
                        result = show_win_screen(screen, n)
                        if result == "start_again":
                            return game_loop(n)  # Relance le jeu avec la même dimension
                        elif result == "main_menu":
                            return show_start_screen # Retourne à l'écran d'accueil

        screen.fill((255, 255, 255))
        draw_grid(screen, puzzle)
        pygame.draw.rect(screen, (0, 128, 0), back_button_rect)
        back_text = font.render("SWAP", True, (255, 255, 255))
        screen.blit(back_text, back_button_rect.topleft)
        pygame.display.flip()
