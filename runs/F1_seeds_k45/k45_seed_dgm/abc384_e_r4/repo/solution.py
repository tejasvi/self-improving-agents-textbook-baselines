# Write your solution here. Read from stdin, write to stdout.

from collections import deque
import sys

def solve():
    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1  # Convert to 0-indexed
    Q -= 1
    
    grid = []
    for _ in range(H):
        row = list(map(int, input().split()))
        grid.append(row)
    
    # BFS/exploration to find maximum strength
    # State: (current_position, absorbed_slimes_bitmask, current_strength)
    # We'll use a simpler approach with DFS + memoization
    
    max_strength = grid[P][Q]
    
    # Use a queue for BFS: (row, col, absorbed_set, current_strength)
    # absorbed_set is a frozenset of absorbed positions
    queue = deque([(P, Q, frozenset(), grid[P][Q])])
    visited = set()
    visited.add((P, Q, frozenset()))
    
    while queue:
        r, c, absorbed, strength = queue.popleft()
        max_strength = max(max_strength, strength)
        
        # Find all adjacent slimes that can be absorbed
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                if (nr, nc) not in absorbed:
                    neighbors.append((nr, nc))
        
        # Try absorbing each neighbor
        for nr, nc in neighbors:
            neighbor_strength = grid[nr][nc]
            # Can absorb if neighbor_strength < strength / X
            # Equivalently: neighbor_strength * X < strength
            if neighbor_strength * X < strength:
                new_strength = strength + neighbor_strength
                new_absorbed = absorbed | frozenset([(nr, nc)])
                state = (r, c, new_absorbed)
                
                if state not in visited:
                    visited.add(state)
                    queue.append((r, c, new_absorbed, new_strength))
    
    print(max_strength)

solve()
