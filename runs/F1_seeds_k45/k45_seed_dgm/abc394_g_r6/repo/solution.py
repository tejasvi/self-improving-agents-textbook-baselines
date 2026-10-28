import heapq
from collections import defaultdict

def solve():
    H, W = map(int, input().split())
    F = []
    for _ in range(H):
        F.append(list(map(int, input().split())))
    
    Q = int(input())
    
    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        # Convert to 0-indexed
        A -= 1
        B -= 1
        C -= 1
        D -= 1
        
        # Use Dijkstra's algorithm
        # State: (cost, i, j, floor)
        # We want to minimize cost (stair usage)
        pq = [(0, A, B, Y)]
        visited = set()
        
        while pq:
            cost, i, j, floor = heapq.heappop(pq)
            
            # Check if we reached the destination
            if i == C and j == D and floor == Z:
                print(cost)
                break
            
            # Skip if already visited this state
            state = (i, j, floor)
            if state in visited:
                continue
            visited.add(state)
            
            # Option 1: Use stairs to go up (if possible)
            if floor < F[i][j]:
                new_state = (i, j, floor + 1)
                if new_state not in visited:
                    heapq.heappush(pq, (cost + 1, i, j, floor + 1))
            
            # Option 2: Use stairs to go down (if possible)
            if floor > 1:
                new_state = (i, j, floor - 1)
                if new_state not in visited:
                    heapq.heappush(pq, (cost + 1, i, j, floor - 1))
            
            # Option 3: Use walkway to adjacent buildings (same floor)
            # Try all 4 adjacent blocks
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W:
                    # Can only move to adjacent building if it has at least 'floor' floors
                    if floor <= F[ni][nj]:
                        new_state = (ni, nj, floor)
                        if new_state not in visited:
                            heapq.heappush(pq, (cost, ni, nj, floor))

solve()
