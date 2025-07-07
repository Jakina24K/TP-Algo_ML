def check_winner(board):
    winning_combinations = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]

    for combo in winning_combinations:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
        
    if all(cell for cell in board):
        return "tie"
    
    return None


def print_board(board):
    for i in range(0, 9, 3):
        row = [cell if cell else str(i + j) for j, cell in enumerate(board[i:i+3])]
        print(" | ".join(row))
        if i < 6:
            print("---------")



def make_move(board, position, player):
    if board[position] == "":
        board[position] = player
        return True
    else:
        print("Case déjà prise. Choisis une autre.")
        return False
    


def switch_player(player):
    return "O" if player == "X" else "X"


def get_ai_move(board):
    # À remplacer par ton algorithme IA
    # Exemple très simple : première case libre
    for i in range(9):
        if board[i] == "":
            return i


def get_player_move(board, player):
    if player == "X":
        # Joueur humain
        while True:
            try:
                position = int(input(f"Joueur {player}, choisis une case (0-8) : "))
                if position < 0 or position > 8:
                    print("Numéro de case invalide.")
                elif board[position] != "":
                    print("Case déjà prise.")
                else:
                    return position
            except ValueError:
                print("Entrez un nombre entier.")
    else:
        # IA
        return get_ai_move(board)


def main():
    board = [""] * 9
    current_player = "X"
    
    while True:
        print_board(board)
        pos = get_player_move(board, current_player)
        make_move(board, pos, current_player)

        result = check_winner(board)
        if result:
            print_board(board)
            if result == "tie":
                print("Match nul !")
            else:
                print(f"Le joueur {result} a gagné !")
            break
        
        current_player = switch_player(current_player)


if __name__ == "__main__":
    main()
