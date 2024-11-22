import pygame
import sys
from logic.puzzle_logic import create_puzzle, move_tile, check_win
from ui.win_screen import show_win_screen
from ui.start_screen import show_start_screen
from logic.solver import solve_puzzle_with_astar

TILE_SIZE = 100

def draw_grid(screen, puzzle):
    """Dessine la grille du puzzle."""
    n = len(puzzle)
    font = pygame.font.Font(None, TILE_SIZE // 2)
    for row in range(n):
        for col in range(n):
            value = puzzle[row][col]
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (200, 200, 200), rect)  # Fond des tuiles
            pygame.draw.rect(screen, (50, 50, 50), rect, 2)  # Contour des tuiles
            if value != 0:
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def game_loop(n, ai_play=False):
    """Boucle principale du jeu."""
    try:
        puzzle = create_puzzle(n)
    except Exception as e:
        print(f"Erreur lors de la création du puzzle : {e}")
        return

    screen = pygame.display.set_mode((n * TILE_SIZE, n * TILE_SIZE + 50))
    pygame.display.set_caption(f"n-Puzzle ({n}x{n})")
    font = pygame.font.Font(None, 36)
    back_button_rect = pygame.Rect(10, n * TILE_SIZE + 10, 100, 30)

    if ai_play:
        solution = solve_puzzle_with_astar(puzzle)
        if solution is None:
            print("Aucune solution trouvée pour ce puzzle.")
            return
        for step in solution:
            puzzle = [list(row) for row in step]
            screen.fill((255, 255, 255))
            draw_grid(screen, puzzle)
            pygame.display.flip()
            pygame.time.delay(500)  # Pause entre chaque étape
        result = show_win_screen(screen, n)  # Affiche "You Win"
        if result == "main_menu":
            return  # Retourne au menu principal
        elif result == "start_again":
            return game_loop(n)  # Relance le jeu avec la même dimension
        return

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button_rect.collidepoint((x, y)):
                    return  # Retourne au menu principal
                if y < n * TILE_SIZE:
                    row, col = y // TILE_SIZE, x // TILE_SIZE
                    move_tile(puzzle, row, col)
                    if check_win(puzzle):
                        result = show_win_screen(screen, n)
                        if result == "main_menu":
                            return  # Retourne au menu principal
                        elif result == "start_again":
                            return game_loop(n)  # Relance le jeu

