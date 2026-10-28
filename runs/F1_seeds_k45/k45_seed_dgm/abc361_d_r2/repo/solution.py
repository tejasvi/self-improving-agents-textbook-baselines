from collections import deque

def solve():
    N = int(input())
    S = input().strip()
    T = input().strip()
    
    # Check if the problem is solvable: counts must match
    if S.count('W') != T.count('W') or S.count('B') != T.count('B'):
        print(-1)
        return
    
    # Initial state: stones followed by 2 empty cells
    initial_state = S + ".."
    target_state = T + ".."
    
    # If already at target
    if initial_state == target_state:
        print(0)
        return
    
    # BFS to find minimum operations
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    
    while queue:
        state, ops = queue.popleft()
        
        # Try all possible moves
        # Find the two empty cells
        empty_pos = []
        for i in range(N + 2):
            if state[i] == '.':
                empty_pos.append(i)
        
        # empty_pos should have exactly 2 elements
        assert len(empty_pos) == 2
        empty1, empty2 = empty_pos[0], empty_pos[1]
        
        # Try moving pairs of adjacent stones
        # We can move stones from position x and x+1 to the empty positions
        for x in range(N + 1):
            if x + 1 < N + 2 and state[x] != '.' and state[x + 1] != '.':
                # We can move the pair at positions x and x+1
                # to positions empty1 and empty2
                
                # Create new state by swapping
                state_list = list(state)
                
                # Store the stones to move
                stone1, stone2 = state_list[x], state_list[x + 1]
                
                # Put them in empty positions (in order)
                if empty1 < empty2:
                    state_list[empty1] = stone1
                    state_list[empty2] = stone2
                else:
                    state_list[empty2] = stone1
                    state_list[empty1] = stone2
                
                # Mark original positions as empty
                state_list[x] = '.'
                state_list[x + 1] = '.'
                
                new_state = ''.join(state_list)
                
                if new_state == target_state:
                    print(ops + 1)
                    return
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, ops + 1))
    
    print(-1)

solve()
