from collections import deque

def solve():
    N = int(input())
    S = input().strip()
    T = input().strip()
    
    # Check if transformation is possible
    # Count of each color must be the same
    if sorted(S) != sorted(T):
        print(-1)
        return
    
    # Initial state: stones in cells 0 to N-1, empty at N and N+1 (0-indexed)
    initial_state = tuple(S) + ('.', '.')
    target_state = tuple(T) + ('.', '.')
    
    if initial_state == target_state:
        print(0)
        return
    
    # BFS
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    
    while queue:
        state, ops = queue.popleft()
        
        # Find empty cells
        empty_pos = [i for i in range(N + 2) if state[i] == '.']
        
        # There should always be exactly 2 empty cells
        k1, k2 = empty_pos[0], empty_pos[1]
        
        # Try all possible moves
        # We need to find adjacent cells with stones at positions x and x+1
        # and move them to empty cells k1 and k2 (in that order)
        
        for x in range(N + 1):
            # Check if cells x and x+1 both have stones
            if x < N + 1 and state[x] != '.' and state[x + 1] != '.':
                # Create new state by moving stones from x and x+1 to k1 and k2
                new_state = list(state)
                new_state[k1] = state[x]
                new_state[k2] = state[x + 1]
                new_state[x] = '.'
                new_state[x + 1] = '.'
                
                new_state = tuple(new_state)
                
                if new_state == target_state:
                    print(ops + 1)
                    return
                
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, ops + 1))
    
    print(-1)

solve()
