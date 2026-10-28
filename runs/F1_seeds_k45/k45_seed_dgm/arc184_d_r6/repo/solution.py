from collections import deque

def solve():
    n = int(input())
    balls = []
    for i in range(n):
        x, y = map(int, input().split())
        balls.append((x, y))
    
    MOD = 998244353
    
    # Use bit representation for states (faster)
    initial_state = (1 << n) - 1  # All bits set
    visited = set()
    queue = deque([initial_state])
    
    def apply_operation(state, k):
        """Apply operation by choosing ball k"""
        if not (state & (1 << k)):
            return state  # Ball k not in state
        
        x_k, y_k = balls[k]
        new_state = (1 << k)  # Keep the chosen ball
        
        for i in range(n):
            if i == k:
                continue
            if not (state & (1 << i)):
                continue  # Ball i not in state
            
            x_i, y_i = balls[i]
            # Check if ball i should be removed
            if (x_i < x_k and y_i < y_k) or (x_i > x_k and y_i > y_k):
                # Remove ball i
                continue
            else:
                # Keep ball i
                new_state |= (1 << i)
        
        return new_state
    
    while queue:
        state = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        
        # Try all possible operations (choose each remaining ball)
        for k in range(n):
            if state & (1 << k):  # Ball k is in state
                next_state = apply_operation(state, k)
                if next_state not in visited:
                    queue.append(next_state)
    
    print(len(visited) % MOD)

solve()
