import pygame
import sys
import aigame
pygame.init()

# Couleurs
BLUE = (10, 10, 63)
LIGHT_BLUE = (100, 160, 255, 120)  # bleu clair translucide (alpha 120)
RED = (255, 60, 56)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)

# Dimensions
WIDTH, HEIGHT = 400, 600
CELL_SIZE = 100
MARGIN = 15  # espace entre cases

# Calcul pour centrer la grille 3x3 avec marges
GRID_WIDTH = 3 * CELL_SIZE + 2 * MARGIN
GRID_ORIGIN_X = (WIDTH - GRID_WIDTH) // 2
GRID_ORIGIN_Y = 200

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Police très grosse et grasse
font = pygame.font.SysFont("Arial", 90, bold=True)

board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"

def check_win_positions():
    for i, row in enumerate(board):
        if row[0] != "" and row.count(row[0]) == 3:
            return row[0], [(i, 0), (i, 1), (i, 2)]
    for col in range(3):
        if board[0][col] != "" and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col], [(0, col), (1, col), (2, col)]
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    return None, None

def draw_grid():
    screen.fill(BLUE)

    winner, win_positions = check_win_positions()

    for i in range(3):
        for j in range(3):
            x = GRID_ORIGIN_X + j * (CELL_SIZE + MARGIN)
            y = GRID_ORIGIN_Y + i * (CELL_SIZE + MARGIN)

            # Ombre pour effet 3D
            shadow_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 50))
            screen.blit(shadow_surface, (x + 5, y + 5))

            cell_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)

            if win_positions and (i, j) in win_positions:
                # Fond opaque jaune ou rouge selon gagnant
                bg_color = YELLOW if winner == "O" else RED
                pygame.draw.rect(cell_surface, bg_color + (255,), (0, 0, CELL_SIZE, CELL_SIZE), border_radius=18)
                # Le symbole dans la même couleur que le fond (pour "effacer")
                symbol = board[i][j]
                if symbol:
                    text = font.render(symbol, True, bg_color)
                    # Centrer le texte
                    text_pos = (
                        (CELL_SIZE - text.get_width()) // 2,
                        (CELL_SIZE - text.get_height()) // 2
                    )
                    cell_surface.blit(text, text_pos)
            else:
                # Fond bleu clair translucide
                pygame.draw.rect(cell_surface, LIGHT_BLUE, (0, 0, CELL_SIZE, CELL_SIZE), border_radius=18)
                # Dessiner le symbole normal (rouge ou jaune)
                symbol = board[i][j]
                if symbol:
                    color = RED if symbol == "X" else YELLOW
                    text = font.render(symbol, True, color)
                    text_pos = (
                        (CELL_SIZE - text.get_width()) // 2,
                        (CELL_SIZE - text.get_height()) // 2
                    )
                    cell_surface.blit(text, text_pos)

            screen.blit(cell_surface, (x, y))

    pygame.display.flip()
def convertBoard(board):
    return [cell for row in board for cell in row]

def convertBoardBack(flat_board):
    return [flat_board[i:i+3] for i in range(0, 9, 3)]

def index_to_coords(index):
    return index // 3, index % 3

def coords_to_index(i, j):
    return i * 3 + j

def get_ai_move2(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                return i, j
    return None

def get_ai_move(b):
    _b = convertBoard(b)
    print(_b)
    aig = aigame.ai_move(_b)
    print(aig)
    print(index_to_coords(aig))
    return index_to_coords(aig)
    return None

def main():
    global current_player, board
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    counter = 0  # Compteur de coups joués

    clock = pygame.time.Clock()
    while True:
        draw_grid()
        winner, _ = check_win_positions()
        if winner:
            import winScreen
            winScreen.main(winner)
            return

        # ✅ Vérifie égalité : 9 coups joués et aucun gagnant
        if counter == 9:
            import egalityScreen
            egalityScreen.main()
            return

        # IA joue
        if current_player == "O":
            pygame.time.delay(200)
            move = get_ai_move(board)
            print(move)
            if move:
                i, j = move
                if board[i][j] == "":
                    board[i][j] = "O"
                    current_player = "X"
                    counter += 1  # ✅ Incrémenter après un coup valide
            continue

        # Joueur humain joue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player == "X":
                x, y = event.pos
                for i in range(3):
                    for j in range(3):
                        cell_x = GRID_ORIGIN_X + j * (CELL_SIZE + MARGIN)
                        cell_y = GRID_ORIGIN_Y + i * (CELL_SIZE + MARGIN)
                        rect = pygame.Rect(cell_x, cell_y, CELL_SIZE, CELL_SIZE)
                        if rect.collidepoint(x, y):
                            if board[i][j] == "":
                                board[i][j] = "X"
                                current_player = "O"
                                counter += 1  # ✅ Incrémenter ici aussi
        clock.tick(60)



if __name__ == "__main__":
    main()
