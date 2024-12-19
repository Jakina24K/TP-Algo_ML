import pygame
import sys
from logic.puzzle_logic import create_puzzle, move_tile, check_win
from ui.win_screen import show_win_screen
from ui.start_screen import show_start_screen
from logic.solver import solve_puzzle_with_astar

TILE_SIZE = 100

def draw_grid(screen, puzzle):
    n = len(puzzle)
    font = pygame.font.Font(None, TILE_SIZE // 2) 

    contour_color = (150, 150, 150)

    for row in range(n):
        for col in range(n):
            value = puzzle[row][col]
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            if value == 0:
                pygame.draw.rect(screen, (255, 255, 255), rect)  # Fond blanc
            else:
                # Cases normales en gris clair
                pygame.draw.rect(screen, (220, 220, 220), rect)  # Fond gris clair
                text = font.render(str(value), True, (0, 0, 0))  # Texte noir
                text_rect = text.get_rect(center=rect.center)  # Centrage du texte
                screen.blit(text, text_rect)  # Affichage du texte

            # Contour de toutes les cases avec une couleur plus douce (gris clair) et une épaisseur plus fine (1)
            pygame.draw.rect(screen, contour_color, rect, 1)  # Contour avec une couleur plus claire


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
        for step in solution:
            puzzle = [list(row) for row in step]
            screen.fill((255, 255, 255))
            draw_grid(screen, puzzle)
            pygame.display.flip()
            pygame.time.delay(200)
        
        result = show_win_screen(screen, n)
            
        if result == "start_again":
            return game_loop(n)
        elif result == "main_menu":
            return show_start_screen()
        return

    move_count = 0 
    swap_mode = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button_rect.collidepoint((x, y)):
                    return
                if y < n * TILE_SIZE:
                    row, col = y // TILE_SIZE, x // TILE_SIZE
                    if move_tile(puzzle, row, col):
                        move_count += 1
                        if move_count == 10:
                            swap_mode = True 
                        if check_win(puzzle):
                            result = show_win_screen(screen, n)
                            if result == "start_again":
                                return game_loop(n)
                            elif result == "main_menu":
                                return show_start_screen()

        screen.fill((255, 255, 255))  # Fond de l'écran

        if swap_mode:
            swap_text = font.render("SWAP", True, (255, 0, 0))
            screen.blit(swap_text, (10, n * TILE_SIZE + 10))
        else:
            move_text = font.render(f"Moves: {move_count}", True, (0, 0, 0))
            screen.blit(move_text, (10, n * TILE_SIZE + 10))

        draw_grid(screen, puzzle)

        pygame.display.flip() 

        if swap_mode:
            swap_tiles(puzzle, screen)
            move_count = 0  
            swap_mode = False 

def swap_tiles(puzzle, screen):
    """Permet au joueur de permuter les valeurs de deux tuiles."""
    font = pygame.font.Font(None, 36)
    selected_tiles = []

    while len(selected_tiles) < 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // TILE_SIZE, x // TILE_SIZE
                if 0 <= row < len(puzzle) and 0 <= col < len(puzzle):
                    selected_tiles.append((row, col))
                    pygame.draw.rect(
                        screen, (255, 0, 0),
                        (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3
                    )
                    pygame.display.flip()

    (row1, col1), (row2, col2) = selected_tiles
    puzzle[row1][col1], puzzle[row2][col2] = puzzle[row2][col2], puzzle[row1][col1]


