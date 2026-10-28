import heapq

def solve():
    N, M = map(int, input().split())
    operations = []
    for _ in range(M):
        L, R = map(int, input().split())
        operations.append((L - 1, R - 1))  # Convert to 0-indexed
    
    # Use Dijkstra's algorithm to find minimum cost assignment
    # State: (covered_positions, op_idx)
    
    if N <= 20:
        # Use bitmask for covered positions
        heap = []
        visited = {}
        parent = {}  # For reconstructing the path
        state_cost = {}  # Cost to reach each state
        
        initial_covered = 0
        heapq.heappush(heap, (0, initial_covered, 0))
        state_cost[(initial_covered, 0)] = 0
        
        target = (1 << N) - 1
        
        while heap:
            cost, covered_mask, op_idx = heapq.heappop(heap)
            
            state = (covered_mask, op_idx)
            if state in visited:
                continue
            visited[state] = True
            
            if op_idx == M:
                # Check if all positions are covered
                if covered_mask == target:
                    # Reconstruct the assignment
                    assignment = [0] * M
                    current_state = state
                    while current_state in parent:
                        prev_state, op_type = parent[current_state]
                        prev_op_idx = current_state[1] - 1
                        assignment[prev_op_idx] = op_type
                        current_state = prev_state
                    
                    print(cost)
                    print(' '.join(map(str, assignment)))
                    return
                continue
            
            # Try operation 0
            new_covered = covered_mask
            new_state = (new_covered, op_idx + 1)
            new_cost = cost
            if new_state not in visited:
                if new_state not in state_cost or state_cost[new_state] > new_cost:
                    state_cost[new_state] = new_cost
                    parent[new_state] = (state, 0)
                    heapq.heappush(heap, (new_cost, new_covered, op_idx + 1))
            
            # Try operation 1
            L, R = operations[op_idx]
            new_covered = covered_mask
            for j in range(L, R + 1):
                new_covered |= (1 << j)
            new_state = (new_covered, op_idx + 1)
            new_cost = cost + 1
            if new_state not in visited:
                if new_state not in state_cost or state_cost[new_state] > new_cost:
                    state_cost[new_state] = new_cost
                    parent[new_state] = (state, 1)
                    heapq.heappush(heap, (new_cost, new_covered, op_idx + 1))
            
            # Try operation 2
            L, R = operations[op_idx]
            new_covered = covered_mask
            for j in range(L):
                new_covered |= (1 << j)
            for j in range(R + 1, N):
                new_covered |= (1 << j)
            new_state = (new_covered, op_idx + 1)
            new_cost = cost + 1
            if new_state not in visited:
                if new_state not in state_cost or state_cost[new_state] > new_cost:
                    state_cost[new_state] = new_cost
                    parent[new_state] = (state, 2)
                    heapq.heappush(heap, (new_cost, new_covered, op_idx + 1))
        
        print(-1)
    else:
        # For large N, use frozenset representation
        heap = []
        visited = {}
        parent = {}  # For reconstructing the path
        state_cost = {}  # Cost to reach each state
        
        initial_covered = frozenset()
        heapq.heappush(heap, (0, initial_covered, 0))
        state_cost[(initial_covered, 0)] = 0
        
        target = frozenset(range(N))
        
        while heap:
            cost, covered, op_idx = heapq.heappop(heap)
            
            state = (covered, op_idx)
            if state in visited:
                continue
            visited[state] = True
            
            if op_idx == M:
                # Check if all positions are covered
                if covered == target:
                    # Reconstruct the assignment
                    assignment = [0] * M
                    current_state = state
                    while current_state in parent:
                        prev_state, op_type = parent[current_state]
                        prev_op_idx = current_state[1] - 1
                        assignment[prev_op_idx] = op_type
                        current_state = prev_state
                    
                    print(cost)
                    print(' '.join(map(str, assignment)))
                    return
                continue
            
            # Try operation 0
            new_covered = covered
            new_state = (new_covered, op_idx + 1)
            new_cost = cost
            if new_state not in visited:
                if new_state not in state_cost or state_cost[new_state] > new_cost:
                    state_cost[new_state] = new_cost
                    parent[new_state] = (state, 0)
                    heapq.heappush(heap, (new_cost, new_covered, op_idx + 1))
            
            # Try operation 1
            L, R = operations[op_idx]
            new_covered = covered | frozenset(range(L, R + 1))
            new_state = (new_covered, op_idx + 1)
            new_cost = cost + 1
            if new_state not in visited:
                if new_state not in state_cost or state_cost[new_state] > new_cost:
                    state_cost[new_state] = new_cost
                    parent[new_state] = (state, 1)
                    heapq.heappush(heap, (new_cost, new_covered, op_idx + 1))
            
            # Try operation 2
            L, R = operations[op_idx]
            complement = frozenset(list(range(L)) + list(range(R + 1, N)))
            new_covered = covered | complement
            new_state = (new_covered, op_idx + 1)
            new_cost = cost + 1
            if new_state not in visited:
                if new_state not in state_cost or state_cost[new_state] > new_cost:
                    state_cost[new_state] = new_cost
                    parent[new_state] = (state, 2)
                    heapq.heappush(heap, (new_cost, new_covered, op_idx + 1))
        
        print(-1)

solve()
