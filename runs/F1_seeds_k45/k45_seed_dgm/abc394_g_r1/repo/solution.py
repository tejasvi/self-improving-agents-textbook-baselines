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
        
        # Dijkstra's algorithm
        # State: (cost, row, col, floor)
        # cost is the number of stair uses
        pq = [(0, A, B, Y)]
        visited = set()
        
        while pq:
            cost, r, c, floor = heapq.heappop(pq)
            
            if r == C and c == D and floor == Z:
                print(cost)
                break
            
            if (r, c, floor) in visited:
                continue
            visited.add((r, c, floor))
            
            # Option 1: Use stairs to go up (if possible)
            if floor < F[r][c]:
                new_floor = floor + 1
                new_cost = cost + 1
                if (r, c, new_floor) not in visited:
                    heapq.heappush(pq, (new_cost, r, c, new_floor))
            
            # Option 2: Use stairs to go down (if possible)
            if floor > 1:
                new_floor = floor - 1
                new_cost = cost + 1
                if (r, c, new_floor) not in visited:
                    heapq.heappush(pq, (new_cost, r, c, new_floor))
            
            # Option 3: Use walkway to adjacent buildings (if they have at least this floor)
            # Try moving to all 4 adjacent cells
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    # Can only move if the adjacent building has at least 'floor' floors
                    if F[nr][nc] >= floor:
                        new_cost = cost  # Walkway is free
                        if (nr, nc, floor) not in visited:
                            heapq.heappush(pq, (new_cost, nr, nc, floor))

solve()
