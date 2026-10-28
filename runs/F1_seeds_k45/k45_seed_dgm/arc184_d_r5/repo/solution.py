def solve():
    MOD = 998244353
    
    n = int(input())
    balls = []
    for _ in range(n):
        x, y = map(int, input().split())
        balls.append((x, y))
    
    # Convert set of ball indices to a frozenset for hashing
    # Start from the full set and explore all reachable states
    
    def perform_operation(state, k):
        """
        Perform operation by choosing ball k (which is in state).
        Remove all balls i in state where:
        (X_i < X_k AND Y_i < Y_k) OR (X_i > X_k AND Y_i > Y_k)
        Return the new state.
        """
        x_k, y_k = balls[k]
        new_state = set()
        for i in state:
            x_i, y_i = balls[i]
            # Check if we should remove ball i
            if (x_i < x_k and y_i < y_k) or (x_i > x_k and y_i > y_k):
                # Remove ball i, don't add to new_state
                pass
            else:
                # Keep ball i
                new_state.add(i)
        return frozenset(new_state)
    
    # BFS to find all reachable states
    initial_state = frozenset(range(n))
    visited = set()
    queue = [initial_state]
    visited.add(initial_state)
    
    while queue:
        current_state = queue.pop(0)
        
        # Try all possible operations from this state
        for k in current_state:
            next_state = perform_operation(current_state, k)
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
    
    print(len(visited) % MOD)

solve()
