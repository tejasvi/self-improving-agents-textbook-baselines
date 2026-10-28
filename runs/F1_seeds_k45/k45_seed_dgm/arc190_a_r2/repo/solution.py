import heapq
from itertools import count

def solve():
    N, M = map(int, input().split())
    operations = []
    for _ in range(M):
        L, R = map(int, input().split())
        operations.append((L-1, R-1))  # Convert to 0-indexed
    
    def merge_intervals_with_complement(intervals, comp_start, comp_end):
        """Merge intervals with complement of [comp_start, comp_end]"""
        # Complement means all positions NOT in [comp_start, comp_end]
        result = list(intervals)
        
        # Add left part [0, comp_start-1]
        if comp_start > 0:
            result.append((0, comp_start - 1))
        
        # Add right part [comp_end+1, N-1]
        if comp_end < N - 1:
            result.append((comp_end + 1, N - 1))
        
        # Now merge overlapping intervals
        if not result:
            return ()
        
        result.sort()
        merged = [result[0]]
        for start, end in result[1:]:
            if start <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        
        return tuple(merged)
    
    def count_covered(key):
        """Count number of covered positions from interval key"""
        return sum(end - start + 1 for start, end in key)
    
    # Use Dijkstra with state = (operation_index, coverage_key)
    initial_key = ()
    
    counter = count()
    heap = [(0, next(counter), 0, initial_key, [])]  # (cost, counter, op_idx, coverage_key, choices)
    visited = {}  # (op_idx, coverage_key) -> min_cost
    
    best_result = None
    best_cost = float('inf')
    
    while heap:
        cost, _, op_idx, coverage_key, choices = heapq.heappop(heap)
        
        # Skip if cost already exceeds best
        if cost >= best_cost:
            continue
        
        # Skip if we've seen this state
        state_key = (op_idx, coverage_key)
        if state_key in visited:
            continue
        visited[state_key] = cost
        
        # If we've processed all operations
        if op_idx == M:
            # Check if all positions are covered
            if count_covered(coverage_key) == N:
                best_cost = cost
                best_result = choices
            continue
        
        L, R = operations[op_idx]
        
        # Try operation 0 (do nothing)
        new_key = coverage_key
        new_cost = cost
        new_choices = choices + [0]
        state = (op_idx + 1, new_key)
        if state not in visited:
            heapq.heappush(heap, (new_cost, next(counter), op_idx + 1, new_key, new_choices))
        
        # Try operation 1 (set [L, R] to 1)
        # Add interval [L, R] to coverage
        new_intervals = list(coverage_key) + [(L, R)]
        if new_intervals:
            new_intervals.sort()
            merged = [new_intervals[0]]
            for start, end in new_intervals[1:]:
                if start <= merged[-1][1] + 1:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], end))
                else:
                    merged.append((start, end))
            new_key = tuple(merged)
        else:
            new_key = ()
        new_cost = cost + 1
        new_choices = choices + [1]
        state = (op_idx + 1, new_key)
        if state not in visited:
            heapq.heappush(heap, (new_cost, next(counter), op_idx + 1, new_key, new_choices))
        
        # Try operation 2 (set positions NOT in [L, R] to 1)
        new_key = merge_intervals_with_complement(coverage_key, L, R)
        new_cost = cost + 1
        new_choices = choices + [2]
        state = (op_idx + 1, new_key)
        if state not in visited:
            heapq.heappush(heap, (new_cost, next(counter), op_idx + 1, new_key, new_choices))
    
    if best_result is None:
        print(-1)
    else:
        print(best_cost)
        print(' '.join(map(str, best_result)))

solve()
