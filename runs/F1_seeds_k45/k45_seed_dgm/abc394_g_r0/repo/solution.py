import heapq
from collections import defaultdict

def solve():
    H, W = map(int, input().split())
    F = []
    for _ in range(H):
        F.append(list(map(int, input().split())))
    
    Q = int(input())
    
    for _ in range(Q):
        a, b, y, c, d, z = map(int, input().split())
        # Convert to 0-indexed
        a -= 1
        b -= 1
        c -= 1
        d -= 1
        
        # Dijkstra's algorithm
        # State: (cost, row, col, floor)
        pq = [(0, a, b, y)]
        visited = {}  # (row, col, floor) -> min_cost
        
        ans = float('inf')
        
        while pq:
            cost, r, col, floor = heapq.heappop(pq)
            
            # Check if we reached destination
            if r == c and col == d and floor == z:
                ans = cost
                break
            
            # Skip if we've visited this state with lower cost
            if (r, col, floor) in visited:
                continue
            visited[(r, col, floor)] = cost
            
            # Option 1: Move up/down within the building
            if floor < F[r][col]:
                # Move up
                new_floor = floor + 1
                if (r, col, new_floor) not in visited:
                    heapq.heappush(pq, (cost + 1, r, col, new_floor))
            
            if floor > 1:
                # Move down
                new_floor = floor - 1
                if (r, col, new_floor) not in visited:
                    heapq.heappush(pq, (cost + 1, r, col, new_floor))
            
            # Option 2: Move to adjacent building at same floor
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, col + dc
                if 0 <= nr < H and 0 <= nc < W and F[nr][nc] >= floor:
                    if (nr, nc, floor) not in visited:
                        heapq.heappush(pq, (cost, nr, nc, floor))
        
        print(ans)

solve()
