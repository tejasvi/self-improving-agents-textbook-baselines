import heapq

class IntervalSet:
    """Efficiently represent a set of disjoint intervals using a sorted list"""
    def __init__(self, intervals=None):
        # intervals is a list of (start, end) tuples representing [start, end]
        if intervals is None:
            self.intervals = []
        else:
            self.intervals = sorted(intervals)
            self._merge()
    
    def _merge(self):
        """Merge overlapping intervals"""
        if not self.intervals:
            return
        merged = []
        current_start, current_end = self.intervals[0]
        for start, end in self.intervals[1:]:
            if start <= current_end + 1:
                current_end = max(current_end, end)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = start, end
        merged.append((current_start, current_end))
        self.intervals = merged
    
    def add_interval(self, start, end):
        """Add an interval [start, end]"""
        self.intervals.append((start, end))
        self._merge()
    
    def remove_interval(self, start, end):
        """Remove an interval [start, end]"""
        new_intervals = []
        for s, e in self.intervals:
            if e < start or s > end:
                # No overlap
                new_intervals.append((s, e))
            else:
                # There's overlap, keep the parts outside [start, end]
                if s < start:
                    new_intervals.append((s, start - 1))
                if e > end:
                    new_intervals.append((end + 1, e))
        self.intervals = new_intervals
    
    def is_empty(self):
        return len(self.intervals) == 0
    
    def count_elements(self):
        """Count total number of elements"""
        return sum(end - start + 1 for start, end in self.intervals)
    
    def to_tuple(self):
        return tuple(self.intervals)
    
    @staticmethod
    def from_tuple(t):
        return IntervalSet(list(t))
    
    def __repr__(self):
        return f"IntervalSet({self.intervals})"

def apply_operation(uncovered, L, R, op):
    """Apply operation and return new uncovered intervals"""
    new_uncovered = IntervalSet(uncovered.intervals)
    
    if op == 0:
        pass  # Do nothing
    elif op == 1:
        # Operation 1: cover [L, R], remove from uncovered
        new_uncovered.remove_interval(L, R)
    else:  # op == 2
        # Operation 2: cover everything except [L, R]
        # This means removing everything except [L, R] from uncovered
        # Which means keeping only the intersection with [L, R]
        kept = []
        for s, e in new_uncovered.intervals:
            # Keep only the part that overlaps with [L, R]
            overlap_start = max(s, L)
            overlap_end = min(e, R)
            if overlap_start <= overlap_end:
                kept.append((overlap_start, overlap_end))
        new_uncovered.intervals = kept
    
    return new_uncovered

def solve():
    N, M = map(int, input().split())
    operations = []
    for _ in range(M):
        L, R = map(int, input().split())
        operations.append((L-1, R-1))  # Convert to 0-indexed
    
    # Initial state: all positions [0, N-1] are uncovered
    initial_uncovered = IntervalSet([(0, N-1)])
    initial_state = initial_uncovered.to_tuple()
    
    # Use Dijkstra's algorithm with priority queue
    heap = [(0, initial_state, 0, [])]  # (cost, uncovered_tuple, op_idx, ops)
    visited = {}
    
    best_solution = None
    best_cost = float('inf')
    
    while heap:
        cost, uncovered_tuple, op_idx, ops = heapq.heappop(heap)
        
        # Skip if we've already found a better solution with this exact state
        state_key = (uncovered_tuple, op_idx)
        if state_key in visited:
            continue
        visited[state_key] = cost
        
        # Prune if already worse than best
        if cost >= best_cost:
            continue
        
        # Check if we've processed all operations
        if op_idx == M:
            uncovered = IntervalSet.from_tuple(uncovered_tuple)
            if uncovered.is_empty():  # All covered
                if cost < best_cost:
                    best_cost = cost
                    best_solution = ops
            continue
        
        L, R = operations[op_idx]
        uncovered = IntervalSet.from_tuple(uncovered_tuple)
        
        # Try all 3 operations
        for op_choice in [0, 1, 2]:
            new_cost = cost + (0 if op_choice == 0 else 1)
            
            # Prune if already worse than best
            if new_cost >= best_cost:
                continue
            
            # Apply operation
            new_uncovered = apply_operation(uncovered, L, R, op_choice)
            new_uncovered_tuple = new_uncovered.to_tuple()
            new_state_key = (new_uncovered_tuple, op_idx + 1)
            
            # Only add if we haven't visited this state yet
            if new_state_key not in visited:
                heapq.heappush(heap, (new_cost, new_uncovered_tuple, op_idx + 1, ops + [op_choice]))
    
    if best_solution is None:
        print(-1)
    else:
        print(best_cost)
        print(' '.join(map(str, best_solution)))

solve()
