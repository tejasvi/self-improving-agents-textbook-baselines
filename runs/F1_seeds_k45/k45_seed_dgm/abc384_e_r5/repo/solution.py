from collections import deque

def solve():
    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1  # Convert to 0-indexed
    Q -= 1
    
    grid = []
    for _ in range(H):
        row = list(map(int, input().split()))
        grid.append(row)
    
    # BFS to explore all possible states
    # State: (takahashi_strength, absorbed_set_frozen)
    # absorbed_set_frozen is a frozenset of absorbed positions
    
    initial_strength = grid[P][Q]
    initial_absorbed = frozenset([(P, Q)])
    
    visited = set()
    queue = deque([(initial_strength, initial_absorbed)])
    visited.add(initial_absorbed)
    
    max_strength = initial_strength
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        current_strength, absorbed = queue.popleft()
        max_strength = max(max_strength, current_strength)
        
        # Find all slimes adjacent to Takahashi
        # A slime is adjacent if it's not absorbed and next to any absorbed slime
        adjacent = set()
        for ai, aj in absorbed:
            for di, dj in directions:
                ni, nj = ai + di, aj + dj
                if 0 <= ni < H and 0 <= nj < W and (ni, nj) not in absorbed:
                    adjacent.add((ni, nj))
        
        # Try absorbing each adjacent slime
        for si, sj in adjacent:
            slime_strength = grid[si][sj]
            # Check if we can absorb this slime
            if slime_strength * X < current_strength:
                # We can absorb this slime
                new_strength = current_strength + slime_strength
                new_absorbed = absorbed | frozenset([(si, sj)])
                
                if new_absorbed not in visited:
                    visited.add(new_absorbed)
                    queue.append((new_strength, new_absorbed))
    
    print(max_strength)

solve()
