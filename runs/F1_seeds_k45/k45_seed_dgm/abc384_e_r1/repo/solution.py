# Write your solution here. Read from stdin, write to stdout.

import heapq

def solve():
    H, W, X = map(int, input().split())
    P, Q = map(int, input().split())
    P -= 1  # Convert to 0-indexed
    Q -= 1
    
    grid = []
    for _ in range(H):
        row = list(map(int, input().split()))
        grid.append(row)
    
    # Takahashi's initial strength
    takahashi_strength = grid[P][Q]
    
    # Track which cells have been absorbed
    absorbed = [[False] * W for _ in range(H)]
    absorbed[P][Q] = True
    
    # BFS to find all reachable slimes and their adjacency
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    # Priority queue of (strength, row, col) - min heap
    # This will help us always try to absorb the weakest adjacent slime first
    adjacent = []
    
    # Add initial neighbors to priority queue
    for dr, dc in directions:
        nr, nc = P + dr, Q + dc
        if 0 <= nr < H and 0 <= nc < W:
            heapq.heappush(adjacent, (grid[nr][nc], nr, nc))
    
    # Keep absorbing slimes greedily
    while adjacent:
        strength, r, c = heapq.heappop(adjacent)
        
        # Skip if already absorbed
        if absorbed[r][c]:
            continue
        
        # Check if we can absorb this slime
        if strength < takahashi_strength / X:
            # Absorb it
            takahashi_strength += strength
            absorbed[r][c] = True
            
            # Add newly adjacent slimes
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and not absorbed[nr][nc]:
                    heapq.heappush(adjacent, (grid[nr][nc], nr, nc))
        else:
            # Can't absorb this or any stronger slime from the queue in this iteration
            # But we should still check if there are other weaker slimes we can reach
            # Continue checking the queue
            pass
    
    print(takahashi_strength)

solve()
