from collections import deque

def solve():
    N, M = map(int, input().split())
    operations = []
    for _ in range(M):
        l, r = map(int, input().split())
        operations.append((l, r))
    
    # BFS to find minimum cost path
    # State: (operation_index, frozenset of covered intervals)
    # For efficiency, we'll represent state as a tuple of disjoint intervals
    
    def intervals_to_tuple(intervals):
        """Convert list of (start, end) intervals to sorted tuple"""
        if not intervals:
            return ()
        intervals = sorted(intervals)
        merged = []
        for start, end in intervals:
            if merged and start <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        return tuple(merged)
    
    def is_complete(intervals):
        """Check if intervals cover [1, N]"""
        if not intervals:
            return False
        return len(intervals) == 1 and intervals[0] == (1, N)
    
    def apply_operation(intervals, op_type, L, R):
        """Apply operation and return new intervals"""
        if op_type == 0:
            return intervals
        elif op_type == 1:
            # Set positions [L, R] to 1
            new_intervals = list(intervals) + [(L, R)]
            return intervals_to_tuple(new_intervals)
        else:  # op_type == 2
            # Set positions outside [L, R] to 1
            new_intervals = list(intervals)
            # Add [1, L-1]
            if L > 1:
                new_intervals.append((1, L - 1))
            # Add [R+1, N]
            if R < N:
                new_intervals.append((R + 1, N))
            return intervals_to_tuple(new_intervals)
    
    # BFS
    queue = deque([(0, (), 0)])  # (op_index, intervals, cost)
    visited = {(0, ()): 0}  # (op_index, intervals) -> min_cost
    parent = {}  # for reconstruction
    
    best_state = None
    best_cost = float('inf')
    
    while queue:
        op_idx, intervals, cost = queue.popleft()
        
        if cost > best_cost:
            continue
        
        if op_idx == M:
            if is_complete(intervals):
                if cost < best_cost:
                    best_cost = cost
                    best_state = intervals
            continue
        
        L, R = operations[op_idx]
        
        # Try all three operations
        for op_type in range(3):
            new_intervals = apply_operation(intervals, op_type, L, R)
            new_cost = cost + (1 if op_type != 0 else 0)
            
            state_key = (op_idx + 1, new_intervals)
            
            if state_key not in visited or visited[state_key] > new_cost:
                visited[state_key] = new_cost
                parent[state_key] = (op_idx, intervals, op_type)
                queue.append((op_idx + 1, new_intervals, new_cost))
    
    if best_cost == float('inf'):
        print(-1)
    else:
        # Reconstruct path
        operations_chosen = [0] * M
        state = (M, best_state)
        
        while state in parent:
            prev_op_idx, prev_intervals, op_type = parent[state]
            operations_chosen[prev_op_idx] = op_type
            state = (prev_op_idx, prev_intervals)
        
        print(best_cost)
        print(' '.join(map(str, operations_chosen)))

solve()
