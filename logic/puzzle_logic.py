import random

def create_puzzle(n):
    tiles = list(range(1, n * n)) + [0]
    while True:
        random.shuffle(tiles)
        if is_solvable(tiles, n):
            break
    return [tiles[i * n:(i + 1) * n] for i in range(n)]

def is_solvable(tiles, n):
    inversions = 0
    flat_tiles = [t for t in tiles if t != 0]
    for i in range(len(flat_tiles)):
        for j in range(i + 1, len(flat_tiles)):
            if flat_tiles[i] > flat_tiles[j]:
                inversions += 1
    if n % 2 == 1:
        return inversions % 2 == 0
    else:
        empty_row = tiles.index(0) // n
        return (inversions + empty_row) % 2 == 1

def move_tile(puzzle, row, col):
    n = len(puzzle)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < n and 0 <= nc < n and puzzle[nr][nc] == 0:
            puzzle[nr][nc], puzzle[row][col] = puzzle[row][col], puzzle[nr][nc]
            return True
    return False

def check_win(puzzle):
    """Vérifie si le puzzle est dans l'état de victoire."""
    n = len(puzzle)
    expected_value = 1

    for row in range(n):
        for col in range(n):
            # La dernière case doit être 0
            if row == n - 1 and col == n - 1:
                if puzzle[row][col] != 0:
                    return False
            else:
                if puzzle[row][col] != expected_value:
                    return False
                expected_value += 1

    return True
    

