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
        A -= 1  # Convert to 0-indexed
        B -= 1
        C -= 1
        D -= 1
        
        # Use Dijkstra's algorithm
        # State: (cost, i, j, floor)
        # cost = number of stairs used
        
        pq = [(0, A, B, Y)]
        visited = {}  # (i, j, floor) -> min cost
        
        result = float('inf')
        
        while pq:
            cost, i, j, floor = heapq.heappop(pq)
            
            # Check if we reached the destination
            if i == C and j == D and floor == Z:
                result = cost
                break
            
            # Skip if we've already found a better path to this state
            state = (i, j, floor)
            if state in visited and visited[state] <= cost:
                continue
            visited[state] = cost
            
            # Option 1: Move within the same building using stairs
            # Move up
            if floor < F[i][j]:
                new_floor = floor + 1
                new_cost = cost + 1
                new_state = (i, j, new_floor)
                if new_state not in visited or visited[new_state] > new_cost:
                    heapq.heappush(pq, (new_cost, i, j, new_floor))
            
            # Move down
            if floor > 1:
                new_floor = floor - 1
                new_cost = cost + 1
                new_state = (i, j, new_floor)
                if new_state not in visited or visited[new_state] > new_cost:
                    heapq.heappush(pq, (new_cost, i, j, new_floor))
            
            # Option 2: Move to adjacent building via walkway (free)
            # Can move to adjacent building at same floor if it has at least that many floors
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W:
                    # Can move to (ni, nj) if it has at least 'floor' floors
                    if F[ni][nj] >= floor:
                        new_state = (ni, nj, floor)
                        if new_state not in visited or visited[new_state] > cost:
                            heapq.heappush(pq, (cost, ni, nj, floor))
        
        print(result if result != float('inf') else -1)

solve()
