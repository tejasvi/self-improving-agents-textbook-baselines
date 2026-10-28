from collections import deque

def solve():
    N = int(input())
    S = input().strip()
    T = input().strip()
    
    # Quick check: if the multiset of colors doesn't match, it's impossible
    if sorted(S) != sorted(T):
        print(-1)
        return
    
    # Represent state as a tuple of (cells 1 to N+2, empty_pos)
    # For simplicity, we'll use a string of length N+2 where '.' represents empty
    
    initial_state = S + ".."
    target_state = T + ".."
    
    # BFS to find minimum operations
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    
    while queue:
        current_state, ops = queue.popleft()
        
        # Check if we reached target
        if current_state[:N] == T:
            print(ops)
            return
        
        # Generate all possible next states
        # Find positions of the two empty cells
        empty_positions = [i for i, c in enumerate(current_state) if c == '.']
        
        if len(empty_positions) != 2:
            continue
        
        empty_pos = empty_positions
        
        # Try moving each pair of adjacent stones to the empty cells
        # We need to find pairs of adjacent cells with stones
        for x in range(N + 1):  # x from 0 to N (representing cells 1 to N+1)
            # Check if cells x and x+1 both have stones
            if x + 1 < len(current_state) and current_state[x] != '.' and current_state[x+1] != '.':
                # We can move stones from positions x and x+1 to empty_pos
                stone1 = current_state[x]
                stone2 = current_state[x+1]
                
                # Create new state
                new_state_list = list(current_state)
                
                # Remove stones from x and x+1
                new_state_list[x] = '.'
                new_state_list[x+1] = '.'
                
                # Place stones at empty positions
                empty_pos_sorted = sorted(empty_pos)
                new_state_list[empty_pos_sorted[0]] = stone1
                new_state_list[empty_pos_sorted[1]] = stone2
                
                new_state = ''.join(new_state_list)
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, ops + 1))
    
    # If we get here, target is unreachable
    print(-1)

solve()
