from collections import deque

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    results = []
    
    # For each starting position K
    for k in range(N):
        # BFS to find maximum size
        # State: (remaining_indices_tuple, takahashi_position_in_list, takahashi_size)
        
        max_size = A[k]
        
        # Use BFS with state = (remaining_indices_tuple, position_in_list, current_size)
        initial_state = (tuple(range(N)), k, A[k])
        queue = deque([initial_state])
        # Track best size for each (remaining_indices, pos) pair
        best = {}
        
        while queue:
            remaining_indices, pos, current_size = queue.popleft()
            
            state_key = (remaining_indices, pos)
            if state_key in best and best[state_key] >= current_size:
                continue
            best[state_key] = current_size
            
            max_size = max(max_size, current_size)
            
            # Try absorbing slimes to the left and right
            neighbors = []
            if pos > 0:  # Left neighbor exists
                neighbors.append((pos - 1, 'left'))
            if pos < len(remaining_indices) - 1:  # Right neighbor exists
                neighbors.append((pos + 1, 'right'))
            
            for next_pos, direction in neighbors:
                neighbor_original_idx = remaining_indices[next_pos]
                neighbor_size = A[neighbor_original_idx]
                
                if neighbor_size < current_size:
                    # Can absorb this slime
                    new_remaining = list(remaining_indices)
                    new_remaining.pop(next_pos)
                    new_remaining = tuple(new_remaining)
                    
                    # Update Takahashi's position in the new list
                    if direction == 'left':
                        new_pos = pos - 1
                    else:
                        new_pos = pos  # Position stays same when absorbing right
                    
                    new_size = current_size + neighbor_size
                    next_key = (new_remaining, new_pos)
                    
                    # Only add to queue if this is a better path to this state
                    if next_key not in best or best[next_key] < new_size:
                        queue.append((new_remaining, new_pos, new_size))
        
        results.append(max_size)
    
    print(' '.join(map(str, results)))

solve()
