from collections import deque

def solve():
    N, M = map(int, input().split())
    operations = []
    for _ in range(M):
        L, R = map(int, input().split())
        operations.append((L, R))
    
    def merge_intervals(intervals):
        """Merge overlapping intervals"""
        if not intervals:
            return []
        intervals = sorted(intervals)
        merged = [intervals[0]]
        for start, end in intervals[1:]:
            if start <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        return merged
    
    def apply_op(intervals, op_type, L, R, N):
        """Apply operation and return new intervals"""
        if op_type == 0:
            return tuple(intervals)
        
        intervals = list(intervals)
        
        if op_type == 1:
            # Add [L, R] to covered intervals
            intervals.append((L, R))
        elif op_type == 2:
            # Add everything outside [L, R]
            intervals.append((1, L - 1))
            intervals.append((R + 1, N))
        
        # Remove invalid intervals and merge
        valid_intervals = [(s, e) for s, e in intervals if s <= e and 1 <= s and e <= N]
        merged = merge_intervals(valid_intervals)
        return tuple(merged)
    
    def is_complete(intervals, N):
        """Check if intervals cover [1, N]"""
        if not intervals:
            return False
        merged = merge_intervals(list(intervals))
        return len(merged) == 1 and merged[0][0] == 1 and merged[0][1] == N
    
    # BFS to find minimum cost
    initial_state = tuple()
    queue = deque([(initial_state, 0, [])])
    visited = {}
    visited[initial_state] = 0
    
    best_cost = float('inf')
    best_ops = None
    
    while queue:
        state, cost, ops = queue.popleft()
        
        if cost >= best_cost:
            continue
        
        op_idx = len(ops)
        
        if op_idx == M:
            if is_complete(state, N):
                if cost < best_cost:
                    best_cost = cost
                    best_ops = ops[:]
            continue
        
        L, R = operations[op_idx]
        
        for op_type in [0, 1, 2]:
            new_state = apply_op(state, op_type, L, R, N)
            new_cost = cost + (1 if op_type != 0 else 0)
            
            # Only explore if we haven't seen this state with lower cost at this operation index
            state_key = (op_idx + 1, new_state)
            if state_key not in visited or visited[state_key] > new_cost:
                visited[state_key] = new_cost
                queue.append((new_state, new_cost, ops + [op_type]))
    
    if best_ops is None:
        print(-1)
    else:
        print(best_cost)
        print(' '.join(map(str, best_ops)))

solve()
