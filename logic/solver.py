import heapq
import time
import csv
from datetime import datetime


def solve_puzzle_with_astar(puzzle):
    """Résout le n-puzzle en utilisant l'algorithme A*."""
    n = len(puzzle)
    start = tuple(tuple(row) for row in puzzle)
    goal = generate_goal_state(n)

    def heuristic(state):
        """Calcule la distance de Manhattan comme heuristique."""
        distance = 0
        for r in range(len(state)):
            for c in range(len(state)):
                value = state[r][c]
                if value == 0:  # Ignorer la case vide
                    continue
                target_r, target_c = divmod(value - 1, len(state))
                distance += abs(target_r - r) + abs(target_c - c)
        return distance

    def neighbors(state):
        """Génère les voisins possibles d'un état."""
        state = [list(row) for row in state]
        zero_row, zero_col = next((r, c) for r in range(n) for c in range(n) if state[r][c] == 0)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in directions:
            nr, nc = zero_row + dr, zero_col + dc
            if 0 <= nr < n and 0 <= nc < n:
                state[zero_row][zero_col], state[nr][nc] = state[nr][nc], state[zero_row][zero_col]
                yield tuple(tuple(row) for row in state)
                state[nr][nc], state[zero_row][zero_col] = state[zero_row][zero_col], state[nr][nc]

    # Début du calcul
    start_time = time.time()
    frontier = [(heuristic(start), 0, start, [])]
    explored = set()
    move_count = 0

    while frontier:
        _, cost, current, path = heapq.heappop(frontier)

        if current == goal:
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Temps en millisecondes
            move_count = len(path)
            export_results(execution_time, move_count, success=True, n=n)
            return path

        if current in explored:
            continue

        explored.add(current)

        for neighbor in neighbors(current):
            if neighbor not in explored:
                heapq.heappush(frontier, (cost + 1 + heuristic(neighbor), cost + 1, neighbor, path + [neighbor]))

    # Pas de solution trouvée
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    export_results(execution_time, move_count, success=False, n=n)
    return None


def generate_goal_state(n):
    """Génère l'état final (objectif) pour une grille de taille n."""
    return tuple(tuple((i * n + j + 1) % (n * n) for j in range(n)) for i in range(n))


def export_results(execution_time, move_count, success, n):
    """Export les résultats dans un fichier CSV."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"puzzle_results_{n}x{n}_{timestamp}.csv"

    # Données à exporter
    results = [
        ["Puzzle Size", "Execution Time (ms)", "Move Count", "Success"],
        [f"{n}x{n}", execution_time, move_count, "Yes" if success else "No"]
    ]

    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(results)

    print(f"Les résultats ont été exportés dans le fichier {file_name}")


# Exemple d'exécution
if __name__ == "__main__":
    # Puzzle 3x3 exemple
    puzzle = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]

    solution = solve_puzzle_with_astar(puzzle)
    if solution:
        print("Solution trouvée avec succès !")
    else:
        print("Pas de solution possible.")
