import heapq

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
