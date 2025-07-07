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