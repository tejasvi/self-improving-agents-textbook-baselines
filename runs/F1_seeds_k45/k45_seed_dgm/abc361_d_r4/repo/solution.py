from collections import deque

def solve():
    N = int(input())
    S = input().strip()
    T = input().strip()
    
    # Check if the stones themselves are the same (just reordered)
    if sorted(S) != sorted(T):
        print(-1)
        return
    
    # Initial state: S + ".."
    initial_state = S + ".."
    target_state = T + ".."
    
    if initial_state == target_state:
        print(0)
        return
    
    # BFS to find minimum operations
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    
    while queue:
        state, ops = queue.popleft()
        
        if state == target_state:
            print(ops)
            return
        
        # Find positions of empty cells
        empty_positions = [i for i in range(N + 2) if state[i] == '.']
        
        if len(empty_positions) != 2:
            continue
        
        empty_pos = sorted(empty_positions)
        
        # Try all possible moves
        # We can move any pair of adjacent stones to the empty positions
        for x in range(N + 1):
            if x < len(state) - 1 and state[x] != '.' and state[x + 1] != '.':
                # We have two adjacent stones at positions x and x+1
                # Move them to empty_pos[0] and empty_pos[1]
                
                state_list = list(state)
                # Clear the stones from x and x+1
                stone1 = state_list[x]
                stone2 = state_list[x + 1]
                state_list[x] = '.'
                state_list[x + 1] = '.'
                # Place them at empty positions
                state_list[empty_pos[0]] = stone1
                state_list[empty_pos[1]] = stone2
                
                new_state = ''.join(state_list)
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, ops + 1))
    
    print(-1)

solve()
