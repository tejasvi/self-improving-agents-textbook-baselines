from collections import deque

def solve():
    # Read input
    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1  # Convert to 0-indexed
    Q -= 1
    
    grid = []
    for _ in range(H):
        row = list(map(int, input().split()))
        grid.append(row)
    
    # BFS to explore all possible sequences of absorptions
    # State: (row, col, strength, absorbed_set)
    visited = set()
    queue = deque([(P, Q, grid[P][Q], frozenset())])
    max_strength = grid[P][Q]
    
    while queue:
        r, c, strength, absorbed = queue.popleft()
        
        # Check if we've seen this state before
        state_key = (r, c, absorbed)
        if state_key in visited:
            continue
        visited.add(state_key)
        
        max_strength = max(max_strength, strength)
        
        # Find all adjacent slimes (not yet absorbed)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                if (nr, nc) not in absorbed:
                    slime_strength = grid[nr][nc]
                    # Can absorb if slime_strength < strength / X
                    if slime_strength * X < strength:
                        new_strength = strength + slime_strength
                        new_absorbed = frozenset(absorbed | {(nr, nc)})
                        new_state_key = (nr, nc, new_absorbed)
                        if new_state_key not in visited:
                            queue.append((nr, nc, new_strength, new_absorbed))
    
    print(max_strength)

solve()
