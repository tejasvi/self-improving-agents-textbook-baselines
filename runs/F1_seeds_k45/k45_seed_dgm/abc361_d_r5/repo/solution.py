from collections import deque

def solve():
    n = int(input())
    s = input().strip()
    t = input().strip()
    
    # Check if transformation is possible
    # The multiset of stones must be the same
    if sorted(s) != sorted(t):
        print(-1)
        return
    
    # BFS to find minimum operations
    # State: tuple of (stones, empty_positions)
    # We represent state as a tuple of length n+2 where each element is 'B', 'W', or '.'
    
    initial_state = tuple(s + "..")
    target_state = tuple(t + "..")
    
    if initial_state == target_state:
        print(0)
        return
    
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    
    while queue:
        state, ops = queue.popleft()
        
        if state == target_state:
            print(ops)
            return
        
        # Find empty positions
        empty_positions = [i for i in range(n + 2) if state[i] == '.']
        
        # Try all possible moves
        # We need to move two adjacent stones to the two empty cells
        for x in range(n + 1):  # x from 1 to N+1 in problem (0 to N in 0-indexed)
            # Check if cells x and x+1 both contain stones
            if state[x] != '.' and state[x + 1] != '.':
                # These are the two stones we want to move
                stone1, stone2 = state[x], state[x + 1]
                
                # Find the two empty cells (k and k+1)
                empty = [i for i in range(n + 2) if state[i] == '.']
                if len(empty) == 2:
                    k1, k2 = empty[0], empty[1]
                    
                    # Check if k2 = k1 + 1 (they must be adjacent)
                    if k2 == k1 + 1:
                        # Perform the move
                        state_list = list(state)
                        state_list[x] = '.'
                        state_list[x + 1] = '.'
                        state_list[k1] = stone1
                        state_list[k2] = stone2
                        new_state = tuple(state_list)
                        
                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_state, ops + 1))
    
    # If we exhaust the queue without finding target, it's impossible
    print(-1)

solve()
