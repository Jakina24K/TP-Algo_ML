import joblib
import pandas as pd

model = joblib.load(r"C:\Users\admin\Desktop\TP-Algo_ML\FINAL EXAM ML\Server\tictactoe_ai_model.pkl")

board = ['b'] * 9

# Affichage du plateau
def print_board(b):
    symbols = {'x': 'X', 'o': 'O', 'b': ' '}
    for i in range(0, 9, 3):
        print(f"{symbols[b[i]]} | {symbols[b[i+1]]} | {symbols[b[i+2]]}")
        if i < 6:
            print("--+---+--")

# Vérifie si un joueur a gagné
def check_winner(b, player):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    return any(all(b[i] == player for i in combo) for combo in wins)

# Vérifie si la partie est terminée
def game_over(b):
    return 'b' not in b or check_winner(b, 'x') or check_winner(b, 'o')

# IA choisit le meilleur coup avec le modèle
def ai_move(b):
    df = pd.DataFrame([b], columns=[f"cell_{i}" for i in range(9)])
    df_encoded = pd.get_dummies(df)

    # Ajouter les colonnes manquantes
    for col in model.feature_names_in_:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    df_encoded = df_encoded[model.feature_names_in_]

    proba = model.predict_proba(df_encoded)[0]
    classes = model.classes_

    # Filtrer les coups légaux uniquement
    legal_moves = [i for i in range(9) if b[i] == 'b']

    # Associer chaque classe connue à sa proba
    class_proba_map = {int(c): p for c, p in zip(classes, proba)}

    # Filtrer seulement les coups légaux connus
    legal_probs = [(i, class_proba_map.get(i, 0)) for i in legal_moves]

    # Choisir le meilleur coup parmi les légaux
    move = max(legal_probs, key=lambda x: x[1])[0]
    return move


# Jeu principal
def play_game():
    print("Bienvenue dans Tic-Tac-Toe contre une IA entraînée (Random Forest)")
    print("Tu es le joueur O. L'IA est X.")
    print("Les cases sont numérotées de 1 à 9 de gauche à droite.")
    print_board(board)

    while not game_over(board):
        # Joueur humain
        while True:
            try:
                move = int(input("Votre coup (1-9) : ")) - 1
                if 0 <= move <= 8 and board[move] == 'b':
                    board[move] = 'o'
                    break
                else:
                    print("Case invalide ou occupée.")
            except:
                print("Entrée invalide.")

        print("\nAprès votre coup :")
        print_board(board)
        if check_winner(board, 'o'):
            print("🎉 Félicitations, vous avez gagné !")
            return
        if game_over(board):
            break

        # Tour de l'IA
        move = ai_move(board.copy())
        if board[move] == 'b':
            board[move] = 'x'
            print("\nL'IA joue :")
            print_board(board)
            if check_winner(board, 'x'):
                print("🤖 L'IA a gagné. Bon essai !")
                return
        else:
            print("⚠️ L'IA a prédit une case occupée. (Rare erreur)")
            return

    print("Match nul !")

# Lancer la partie
play_game()
