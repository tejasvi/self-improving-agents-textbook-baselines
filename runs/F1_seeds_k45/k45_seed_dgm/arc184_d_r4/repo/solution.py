#!/usr/bin/env python3

def solve():
    N = int(input())
    balls = []
    for _ in range(N):
        x, y = map(int, input().split())
        balls.append((x, y))
    
    MOD = 998244353
    
    # BFS to find all reachable states (sets of remaining balls)
    # State is represented as a frozenset of ball indices
    initial_state = frozenset(range(N))
    visited = {initial_state}
    queue = [initial_state]
    
    def get_next_states(state):
        """Get all states reachable by performing one operation on the given state"""
        next_states = []
        state_list = list(state)
        
        # Try removing each ball
        for k in state_list:
            x_k, y_k = balls[k]
            # Find balls to remove when we choose ball k
            to_remove = set()
            
            for i in state_list:
                if i == k:
                    continue
                x_i, y_i = balls[i]
                # Remove ball i if it dominates k or is dominated by k
                if (x_i < x_k and y_i < y_k) or (x_i > x_k and y_i > y_k):
                    to_remove.add(i)
            
            # Also remove k itself
            to_remove.add(k)
            
            new_state = frozenset(state - to_remove)
            next_states.append(new_state)
        
        return next_states
    
    while queue:
        current_state = queue.pop(0)
        
        for next_state in get_next_states(current_state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
    
    print(len(visited) % MOD)

solve()
