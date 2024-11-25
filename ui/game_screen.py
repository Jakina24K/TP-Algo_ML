import pygame
import sys
from logic.puzzle_logic import create_puzzle, move_tile, check_win
from ui.win_screen import show_win_screen
from ui.start_screen import show_start_screen
from logic.solver import solve_puzzle_with_astar

TILE_SIZE = 100

def draw_grid(screen, puzzle):
    n = len(puzzle)
    font = pygame.font.Font(None, TILE_SIZE // 2)  # Police pour le texte

    # Couleur plus douce pour les contours (gris clair)
    contour_color = (150, 150, 150)  # Gris clair pour les contours

    for row in range(n):
        for col in range(n):
            value = puzzle[row][col]
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            if value == 0:
                # Case vide en blanc
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
            pygame.time.delay(200)  # Pause entre chaque étape
        
        result = show_win_screen(screen, n)
            
        if result == "start_again":
            return game_loop(n)
        elif result == "main_menu":
            return show_start_screen()  # Affiche "You Win"
        return

    move_count = 0  # Compteur de mouvements
    swap_mode = False  # Mode d'échange de tuiles

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
                    if move_tile(puzzle, row, col):  # Déplacement valide
                        move_count += 1  # Incrémente le compteur
                        if move_count == 10:
                            swap_mode = True  # Passe en mode "SWAP"
                        if check_win(puzzle):
                            result = show_win_screen(screen, n)
                            if result == "start_again":
                                return game_loop(n)  # Relance le jeu avec la même dimension
                            elif result == "main_menu":
                                # Rediriger vers l'écran principal
                                return show_start_screen() # Retourne à l'écran d'accueil

        # Mettre à jour l'écran
        screen.fill((255, 255, 255))  # Fond de l'écran

        # Si le mode "SWAP" est activé, afficher "SWAP" au lieu de "Moves"
        if swap_mode:
            swap_text = font.render("SWAP", True, (255, 0, 0))
            screen.blit(swap_text, (10, n * TILE_SIZE + 10))
        else:
            # Afficher le nombre de mouvements
            move_text = font.render(f"Moves: {move_count}", True, (0, 0, 0))
            screen.blit(move_text, (10, n * TILE_SIZE + 10))

        # Dessiner la grille
        draw_grid(screen, puzzle)

        pygame.display.flip()  # Met à jour l'affichage

        # Si le mode "SWAP" est activé, effectuer l'échange de tuiles
        if swap_mode:
            swap_tiles(puzzle, screen)
            move_count = 0  # Réinitialise le compteur de mouvements après l'échange
            swap_mode = False  # Désactive le mode "SWAP"

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

    # Échanger les valeurs
    (row1, col1), (row2, col2) = selected_tiles
    puzzle[row1][col1], puzzle[row2][col2] = puzzle[row2][col2], puzzle[row1][col1]


