from collections import deque

def solve():
    N = int(input())
    S = input().strip()
    T = input().strip()
    
    # Initial state: stones in cells 0 to N-1, empty at N and N+1
    initial = S + ".."
    target = T + ".."
    
    # Check if the multiset of stones is the same
    if sorted(S) != sorted(T):
        print(-1)
        return
    
    # BFS to find minimum operations
    if initial == target:
        print(0)
        return
    
    visited = {initial}
    queue = deque([(initial, 0)])
    
    while queue:
        state, ops = queue.popleft()
        
        # Find positions of empty cells
        empty_positions = [i for i in range(N + 2) if state[i] == '.']
        
        # Empty positions should always be exactly 2
        if len(empty_positions) != 2:
            continue
        
        e1, e2 = empty_positions[0], empty_positions[1]
        
        # The empty cells must be adjacent to perform reverse operation
        # If empty cells are at positions e1 and e2 (e1 < e2)
        # We can take stones from adjacent positions that are not empty
        
        # Try all possible moves: pick two adjacent cells with stones
        for x in range(N + 1):
            # Check if cells x and x+1 both have stones
            if state[x] != '.' and state[x + 1] != '.':
                # Move stones from x and x+1 to empty positions
                # The empty positions are e1 and e2
                # Stones go to e1 and e2 in order
                
                state_list = list(state)
                # Place stones at empty positions
                state_list[e1] = state[x]
                state_list[e2] = state[x + 1]
                # Clear original positions
                state_list[x] = '.'
                state_list[x + 1] = '.'
                
                new_state = ''.join(state_list)
                
                if new_state == target:
                    print(ops + 1)
                    return
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, ops + 1))
    
    print(-1)

solve()
