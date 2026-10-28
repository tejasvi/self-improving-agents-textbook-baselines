from collections import deque

def solve():
    N = int(input())
    S = input().strip()
    T = input().strip()
    
    # Check if transformation is possible
    # The multiset of stones must be the same
    if sorted(S) != sorted(T):
        print(-1)
        return
    
    # Initial state: S + ".." (two empty cells at the end)
    initial_state = S + ".."
    # Target state: T + ".." (we need to reach this)
    target_state = T + ".."
    
    # BFS to find minimum operations
    queue = deque([(initial_state, 0)])  # (state, num_operations)
    visited = {initial_state}
    
    while queue:
        state, ops = queue.popleft()
        
        # Check if we reached the target
        if state == target_state:
            print(ops)
            return
        
        # Generate all possible next states
        # Find positions of the two empty cells
        empty_positions = [i for i, c in enumerate(state) if c == '.']
        
        if len(empty_positions) != 2:
            continue
        
        k1, k2 = empty_positions[0], empty_positions[1]
        
        # Try all possible x values (positions from which we move two adjacent stones)
        for x in range(N + 1):  # x ranges from 0 to N (0-indexed)
            # Check if cells x and x+1 both contain stones (0-indexed)
            if x + 1 < len(state) and state[x] != '.' and state[x + 1] != '.':
                # Move stones from positions x and x+1 to k1 and k2
                # Create new state
                state_list = list(state)
                
                # Move stones from x, x+1 to k1, k2
                state_list[k1] = state[x]
                state_list[k2] = state[x + 1]
                state_list[x] = '.'
                state_list[x + 1] = '.'
                
                new_state = ''.join(state_list)
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, ops + 1))
    
    # If we couldn't reach the target state
    print(-1)

solve()
