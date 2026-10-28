from collections import deque

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    results = []
    
    # For each starting position K
    for k in range(N):
        # BFS to find maximum size Takahashi can reach
        # State: (remaining_slimes_tuple, takahashi_size, takahashi_index_in_remaining)
        initial_remaining = tuple(range(N))
        initial_size = A[k]
        initial_index = k
        
        # Use a set to track visited states to avoid revisiting
        visited = set()
        max_size = initial_size
        
        queue = deque([(initial_remaining, initial_size, initial_index)])
        visited.add((initial_remaining, initial_size, initial_index))
        
        while queue:
            remaining, size, idx = queue.popleft()
            
            max_size = max(max_size, size)
            
            # Find current position of Takahashi in the remaining list
            current_pos = remaining.index(idx)
            
            # Try absorbing left neighbor if it exists and is smaller
            if current_pos > 0:
                left_original_idx = remaining[current_pos - 1]
                if A[left_original_idx] < size:
                    new_remaining = remaining[:current_pos - 1] + remaining[current_pos:]
                    new_size = size + A[left_original_idx]
                    new_pos = current_pos - 1
                    state = (new_remaining, new_size, idx)
                    if state not in visited:
                        visited.add(state)
                        queue.append((new_remaining, new_size, idx))
            
            # Try absorbing right neighbor if it exists and is smaller
            if current_pos < len(remaining) - 1:
                right_original_idx = remaining[current_pos + 1]
                if A[right_original_idx] < size:
                    new_remaining = remaining[:current_pos + 1] + remaining[current_pos + 2:]
                    new_size = size + A[right_original_idx]
                    state = (new_remaining, new_size, idx)
                    if state not in visited:
                        visited.add(state)
                        queue.append((new_remaining, new_size, idx))
        
        results.append(max_size)
    
    print(' '.join(map(str, results)))

solve()
