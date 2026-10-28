# Write your solution here. Read from stdin, write to stdout.

from collections import deque

def solve():
    # Read input
    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1  # Convert to 0-indexed
    Q -= 1
    
    grid = []
    for i in range(H):
        row = list(map(int, input().split()))
        grid.append(row)
    
    # BFS to find maximum strength
    # State: (position_r, position_c, strength, absorbed_set)
    # absorbed_set is a frozenset of (r, c) positions that have been absorbed
    
    queue = deque()
    visited = set()
    
    initial_strength = grid[P][Q]
    initial_state = (P, Q, initial_strength, frozenset())
    queue.append(initial_state)
    
    max_strength = initial_strength
    
    while queue:
        pos_r, pos_c, strength, absorbed = queue.popleft()
        
        # Create a state key for visited check
        state_key = (pos_r, pos_c, absorbed)
        if state_key in visited:
            continue
        visited.add(state_key)
        
        max_strength = max(max_strength, strength)
        
        # Try to absorb adjacent slimes
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in directions:
            nr, nc = pos_r + dr, pos_c + dc
            
            # Check bounds
            if 0 <= nr < H and 0 <= nc < W:
                # Check if not already absorbed
                if (nr, nc) not in absorbed:
                    slime_strength = grid[nr][nc]
                    # Check if we can absorb (strictly less than 1/X times our strength)
                    if slime_strength * X < strength:
                        new_strength = strength + slime_strength
                        new_absorbed = absorbed | {(nr, nc)}
                        new_state = (nr, nc, new_strength, new_absorbed)
                        new_state_key = (nr, nc, new_absorbed)
                        
                        if new_state_key not in visited:
                            queue.append(new_state)
    
    print(max_strength)

solve()
