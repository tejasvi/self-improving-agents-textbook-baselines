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
    
    initial_strength = grid[P][Q]
    
    # BFS approach
    # State: (pos_i, pos_j, strength, absorbed_tuple)
    # absorbed_tuple is a sorted tuple of (i,j) coordinates
    
    queue = deque([(P, Q, initial_strength, tuple([(P, Q)]))])
    visited = set()
    visited.add((P, Q, initial_strength, tuple([(P, Q)])))
    
    max_strength = initial_strength
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        pos_i, pos_j, strength, absorbed_tuple = queue.popleft()
        max_strength = max(max_strength, strength)
        
        absorbed_set = set(absorbed_tuple)
        
        # Find all adjacent slimes that can be absorbed
        for di, dj in directions:
            ni, nj = pos_i + di, pos_j + dj
            
            # Check bounds
            if 0 <= ni < H and 0 <= nj < W:
                # Check if not already absorbed
                if (ni, nj) not in absorbed_set:
                    slime_strength = grid[ni][nj]
                    # Check if we can absorb (strictly less than strength/X)
                    if slime_strength * X < strength:
                        new_absorbed = tuple(sorted(absorbed_set | {(ni, nj)}))
                        new_strength = strength + slime_strength
                        new_state = (ni, nj, new_strength, new_absorbed)
                        
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append(new_state)
    
    print(max_strength)

solve()
