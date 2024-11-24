import pygame
import sys
from logic.puzzle_logic import create_puzzle, move_tile, check_win
from ui.win_screen import show_win_screen
from ui.start_screen import show_start_screen
import heapq

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

def solve_puzzle_with_astar(puzzle):
    """Résout le puzzle en utilisant A*."""
    n = len(puzzle)
    start = tuple(tuple(row) for row in puzzle)
    goal = tuple(tuple((i * n + j + 1) % (n * n) for j in range(n)) for i in range(n))

    def heuristic(state):
        """Calcule l'heuristique (distance de Manhattan)."""
        distance = 0
        for r in range(n):
            for c in range(n):
                value = state[r][c]
                if value == 0:
                    continue
                target_r, target_c = divmod(value - 1, n)
                distance += abs(target_r - r) + abs(target_c - c)
        return distance

    def neighbors(state):
        """Retourne les états voisins."""
        state = [list(row) for row in state]
        zero_row, zero_col = next((r, c) for r in range(n) for c in range(n) if state[r][c] == 0)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = zero_row + dr, zero_col + dc
            if 0 <= nr < n and 0 <= nc < n:
                state[zero_row][zero_col], state[nr][nc] = state[nr][nc], state[zero_row][zero_col]
                yield tuple(tuple(row) for row in state)
                state[nr][nc], state[zero_row][zero_col] = state[zero_row][zero_col], state[nr][nc]

    frontier = [(heuristic(start), 0, start, [])]
    explored = set()

    while frontier:
        _, cost, current, path = heapq.heappop(frontier)

        if current == goal:
            return path

        if current in explored:
            continue

        explored.add(current)

        for neighbor in neighbors(current):
            if neighbor not in explored:
                heapq.heappush(frontier, (cost + 1 + heuristic(neighbor), cost + 1, neighbor, path + [neighbor]))

    return None  # Pas de solution

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
            pygame.time.delay(500)  # Pause entre chaque étape
        show_win_screen(screen, n)  # Affiche "You Win"
        return

    move_count = 0  # Compteur de mouvements

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
                        if check_win(puzzle):
                            result = show_win_screen(screen, n)
                            if result == "start_again":
                                return game_loop(n)  # Relance le jeu avec la même dimension
                            elif result == "main_menu":
                                # Rediriger vers l'écran principal
                                return show_start_screen() # Retourne à l'écran d'accueil

        # Vérifier si le joueur a atteint 10 mouvements
        if move_count == 10:
            swap_tiles(puzzle, screen)
            move_count = 0  # Réinitialise le compteur

        # Mettre à jour l'écran
        screen.fill((255, 255, 255))
        draw_grid(screen, puzzle)

        # Afficher le compteur de mouvements
        move_text = font.render(f"Moves: {move_count}", True, (0, 0, 0))
        screen.blit(move_text, (10, n * TILE_SIZE + 10))

        pygame.display.flip()


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


