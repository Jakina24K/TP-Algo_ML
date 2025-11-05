import pandas as pd

# Vérifie les conditions de victoire
def check_winner(board, player):
    win_cond = [(0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6)]
    return any(all(board[i] == player for i in cond) for cond in win_cond)

# Vérifie si le jeu est fini
def is_terminal(board):
    return check_winner(board, 'x') or check_winner(board, 'o') or 'b' not in board

# Minimax récursif
def minimax_move(board, player):
    opponent = 'o' if player == 'x' else 'x'

    if check_winner(board, player):
        return 1
    if check_winner(board, opponent):
        return -1
    if 'b' not in board:
        return 0

    best_score = -float('inf')
    best_move = None

    for i in range(9):
        if board[i] == 'b':
            board[i] = player
            score = -minimax_score(board, opponent)
            board[i] = 'b'
            if score > best_score:
                best_score = score
                best_move = i

    return best_move

def minimax_score(board, player):
    opponent = 'o' if player == 'x' else 'x'

    if check_winner(board, player):
        return 1
    if check_winner(board, opponent):
        return -1
    if 'b' not in board:
        return 0

    best_score = -float('inf')
    for i in range(9):
        if board[i] == 'b':
            board[i] = player
            score = -minimax_score(board, opponent)
            board[i] = 'b'
            best_score = max(best_score, score)

    return best_score

dataset = []

def generate(board, player):
    if is_terminal(board): return
    move = minimax_move(board.copy(), player)
    if isinstance(move, int) and board[move] == 'b':
        dataset.append(board.copy() + [move])
    for i in range(9):
        if board[i] == 'b':
            board[i] = player
            generate(board, 'o' if player == 'x' else 'x')
            board[i] = 'b'
# Exécution
generate(['b']*9, 'x')

# Enregistrement dans un CSV
df = pd.DataFrame(dataset, columns=[f'cell_{i}' for i in range(9)] + ['best_move'])
df.to_csv("tic_tac_toe_minimax_dataset.csv", index=False)
print("Dataset généré avec succès ✅")
