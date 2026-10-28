import heapq

def solve():
    H, W = map(int, input().split())
    F = []
    for _ in range(H):
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
        # State: (cost, row, col, floor)
        pq = [(0, A, B, Y)]
        visited = {}  # (row, col, floor) -> min_cost
        
        result = float('inf')
        
        while pq:
            cost, r, c, floor = heapq.heappop(pq)
            
            # Check if we reached the destination
            if r == C and c == D and floor == Z:
                result = cost
                break
            
            # Skip if we've already visited this state with better cost
            state = (r, c, floor)
            if state in visited:
                continue
            visited[state] = cost
            
            max_floor = F[r][c]
            
            # For each adjacent building, determine which floors are worth visiting
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if not (0 <= nr < H and 0 <= nc < W):
                    continue
                
                target_max = F[nr][nc]
                
                # Determine which floors in current building we can use to move
                # We can move to adjacent building at any floor <= both buildings' heights
                max_reachable = min(max_floor, target_max)
                
                # Critical floors to try: current floor, destination floor, and target building height
                floors_to_try = set()
                
                if floor <= max_reachable:
                    floors_to_try.add(floor)
                
                if nr == C and nc == D and Z <= max_reachable:
                    floors_to_try.add(Z)
                
                floors_to_try.add(max_reachable)
                
                for next_floor in floors_to_try:
                    if 1 <= next_floor <= target_max:
                        stair_cost = abs(floor - next_floor)
                        new_cost = cost + stair_cost
                        next_state = (nr, nc, next_floor)
                        if next_state not in visited:
                            heapq.heappush(pq, (new_cost, nr, nc, next_floor))
        
        print(result if result != float('inf') else -1)

solve()
