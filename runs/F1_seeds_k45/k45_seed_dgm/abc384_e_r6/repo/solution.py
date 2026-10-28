import sys
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
    
    # Start position and initial strength
    takahashi_strength = grid[P][Q]
    
    # Track which slimes have been absorbed
    absorbed = [[False] * W for _ in range(H)]
    absorbed[P][Q] = True
    
    # BFS/Greedy approach: continuously find the weakest adjacent slime
    # that can be absorbed and absorb it
    
    while True:
        # Find all slimes adjacent to Takahashi that can be absorbed
        # We need to track the region Takahashi occupies
        # Since slimes disappear and the gap is filled, Takahashi expands
        
        # Find all cells reachable from (P, Q) that are absorbed
        reachable = set()
        queue = deque([(P, Q)])
        reachable.add((P, Q))
        
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and absorbed[nr][nc] and (nr, nc) not in reachable:
                    reachable.add((nr, nc))
                    queue.append((nr, nc))
        
        # Find all adjacent slimes to the reachable region
        candidates = []
        for r, c in reachable:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and not absorbed[nr][nc]:
                    slime_strength = grid[nr][nc]
                    # Check if this slime can be absorbed
                    if slime_strength * X < takahashi_strength:
                        candidates.append((slime_strength, nr, nc))
        
        if not candidates:
            break
        
        # Greedy: absorb the weakest slime first
        candidates.sort()
        _, nr, nc = candidates[0]
        
        # Absorb the slime
        absorbed[nr][nc] = True
        takahashi_strength += grid[nr][nc]
    
    print(takahashi_strength)

solve()
