import heapq
from collections import defaultdict

def solve():
    H, W = map(int, input().split())
    
    # Read the floor counts for each building
    F = []
    for _ in range(H):
        row = list(map(int, input().split()))
        F.append(row)
    
    Q = int(input())
    
    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        # Convert to 0-indexed
        A -= 1
        B -= 1
        C -= 1
        D -= 1
        
        # Use Dijkstra's algorithm
        # State: (cost, row, col, floor)
        pq = [(0, A, B, Y)]
        visited = set()
        
        while pq:
            cost, r, c, floor = heapq.heappop(pq)
            
            # Check if we reached the target
            if r == C and c == D and floor == Z:
                print(cost)
                break
            
            # Skip if already visited
            if (r, c, floor) in visited:
                continue
            visited.add((r, c, floor))
            
            # Option 1: Use stairs to go up
            if floor < F[r][c]:
                new_floor = floor + 1
                if (r, c, new_floor) not in visited:
                    heapq.heappush(pq, (cost + 1, r, c, new_floor))
            
            # Option 2: Use stairs to go down
            if floor > 1:
                new_floor = floor - 1
                if (r, c, new_floor) not in visited:
                    heapq.heappush(pq, (cost + 1, r, c, new_floor))
            
            # Option 3: Use walkway to adjacent buildings (same floor)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    # Can move to this building if it has at least 'floor' floors
                    if F[nr][nc] >= floor:
                        if (nr, nc, floor) not in visited:
                            heapq.heappush(pq, (cost, nr, nc, floor))

solve()
