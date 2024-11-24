import heapq
import time
import csv  # Bibliothèque pour écrire dans un fichier CSV
from datetime import datetime

def solve_puzzle_with_astar(puzzle):
    """Résout le puzzle en utilisant l'algorithme A*."""
    n = len(puzzle)
    start = tuple(tuple(row) for row in puzzle)
    goal = tuple(tuple((i * n + j + 1) % (n * n) for j in range(n)) for i in range(n))

    def heuristic(state):
        """Calcule la distance de Manhattan pour une heuristique."""
        distance = 0
        for r in range(len(state)):
            for c in range(len(state)):
                value = state[r][c]
                if value < 0 or value >= len(state) ** 2:
                    raise ValueError(f"Valeur incorrecte dans le puzzle : {value}")
                if value == 0:
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
    start_time = int(time.time() * 1000)
    
    frontier = [(heuristic(start), 0, start, [])]
    explored = set()
    move_count = 0  # Nombre de déplacements

    while frontier:
        _, cost, current, path = heapq.heappop(frontier)

        if current == goal:
            end_time = int(time.time() * 1000)  # Temps de fin
            execution_time = end_time - start_time  # Temps d'exécution
            move_count = len(path)  # Nombre de déplacements
            export_results(execution_time, move_count, success=True)  # Exporter les résultats
            return path  # Retourner la solution

        if current in explored:
            continue

        explored.add(current)

        for neighbor in neighbors(current):
            if neighbor not in explored:
                heapq.heappush(frontier, (cost + 1 + heuristic(neighbor), cost + 1, neighbor, path + [neighbor]))         

    # Si pas de solution trouvée
    end_time = time.time()
    execution_time = end_time - start_time
    move_count = 0
    export_results(execution_time, move_count, success=False)
    return None  # Pas de solution

def export_results(execution_time, move_count, success):
    """Export les résultats dans un fichier CSV."""
    # Créer le nom du fichier basé sur la date et l'heure actuelle
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"puzzle_results_{timestamp}.csv"

    # Données à exporter
    results = [
        ["Execution Time (ms)", "Move Count", "Success"],
        [execution_time, move_count, "Yes" if success else "No"]
    ]

    # Écrire dans le fichier CSV
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(results)

    print(f"Les résultats ont été exportés dans le fichier {file_name}")

