import heapq
from collections import defaultdict

def solve():
    H, W = map(int, input().split())
    F = []
    for i in range(H):
        row = list(map(int, input().split()))
        F.append(row)
    
    Q = int(input())
    
    for _ in range(Q):
        A, B, Y, C, D, Z = map(int, input().split())
        A -= 1  # Convert to 0-indexed
        B -= 1
        C -= 1
        D -= 1
        
        # Dijkstra's algorithm
        # State: (cost, i, j, floor)
        pq = [(0, A, B, Y)]
        visited = set()
        
        while pq:
            cost, i, j, floor = heapq.heappop(pq)
            
            # Check if we reached the destination
            if i == C and j == D and floor == Z:
                print(cost)
                break
            
            state = (i, j, floor)
            if state in visited:
                continue
            visited.add(state)
            
            # Option 1: Move up or down in the current building
            # Try moving to floor Z if we're in the destination building
            if i == C and j == D:
                stair_cost = abs(Z - floor)
                new_state = (i, j, Z)
                if new_state not in visited:
                    heapq.heappush(pq, (cost + stair_cost, i, j, Z))
            
            # Try moving to any intermediate floor in this building
            # We should consider moving to floors that might help us reach adjacent buildings
            # Key insight: we only care about floors that are <= heights of adjacent buildings
            
            # Collect all relevant floors in this building
            relevant_floors = set()
            relevant_floors.add(Z if (i == C and j == D) else floor)
            
            # Add floors from adjacent buildings
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W:
                    # We can walkway to adjacent building at any floor <= min(F[i][j], F[ni][nj])
                    relevant_floors.add(min(F[i][j], F[ni][nj]))
                    # Also add the destination floor if applicable
                    if ni == C and nj == D:
                        relevant_floors.add(Z)
            
            # Move to other floors in current building
            for target_floor in relevant_floors:
                if 1 <= target_floor <= F[i][j] and target_floor != floor:
                    stair_cost = abs(target_floor - floor)
                    new_state = (i, j, target_floor)
                    if new_state not in visited:
                        heapq.heappush(pq, (cost + stair_cost, i, j, target_floor))
            
            # Option 2: Use walkway to adjacent building
            # We can walkway to adjacent building if it has at least 'floor' floors
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W and F[ni][nj] >= floor:
                    new_state = (ni, nj, floor)
                    if new_state not in visited:
                        heapq.heappush(pq, (cost, ni, nj, floor))

solve()
