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
        # Convert to 0-indexed
        A -= 1
        B -= 1
        C -= 1
        D -= 1
        
        # Get interesting floors for each building
        def get_interesting_floors(r, c, target_floor=None):
            """Get the set of interesting floors to consider in building (r, c)"""
            interesting = set()
            interesting.add(1)
            interesting.add(F[r][c])
            
            if target_floor is not None:
                interesting.add(target_floor)
            
            # Add floors at adjacent building heights (and one below if possible)
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    interesting.add(F[nr][nc])
                    if F[nr][nc] > 1:
                        interesting.add(F[nr][nc] - 1)
            
            # Only keep floors that are valid for this building
            interesting = {f for f in interesting if 1 <= f <= F[r][c]}
            return interesting
        
        # Dijkstra's algorithm
        # State: (cost, row, col, floor)
        pq = [(0, A, B, Y)]
        visited = set()
        dist = {}
        dist[(A, B, Y)] = 0
        
        while pq:
            cost, r, c, floor = heapq.heappop(pq)
            
            # Skip if we've already processed this state
            state = (r, c, floor)
            if state in visited:
                continue
            visited.add(state)
            
            # Check if we reached destination
            if r == C and c == D and floor == Z:
                print(cost)
                break
            
            # Get interesting floors in this building
            interesting = get_interesting_floors(r, c, Z if r == C and c == D else None)
            
            # Try moving to each interesting floor in this building
            for next_floor in interesting:
                if next_floor == floor:
                    continue
                
                next_state = (r, c, next_floor)
                next_cost = cost + abs(next_floor - floor)
                
                if next_state not in visited and next_cost < dist.get(next_state, float('inf')):
                    dist[next_state] = next_cost
                    heapq.heappush(pq, (next_cost, r, c, next_floor))
            
            # Option 2: Move to adjacent building via walkway
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W:
                    # Can move to (nr, nc, floor) if F[nr][nc] >= floor
                    if F[nr][nc] >= floor:
                        next_state = (nr, nc, floor)
                        if next_state not in visited:
                            heapq.heappush(pq, (cost, nr, nc, floor))

solve()
