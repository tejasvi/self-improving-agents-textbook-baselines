from collections import deque

def solve():
    n = int(input())
    balls = []
    for i in range(n):
        x, y = map(int, input().split())
        balls.append((x, y))
    
    MOD = 998244353
    
    # BFS to find all reachable sets of balls
    # A state is represented as a frozenset of ball indices
    initial_state = frozenset(range(n))
    visited = {initial_state}
    queue = deque([initial_state])
    
    while queue:
        current_set = queue.popleft()
        
        # Try all possible operations
        # For each ball k in current_set, perform operation and see what remains
        for k in current_set:
            x_k, y_k = balls[k]
            
            # Determine which balls would be removed if we choose ball k
            removed = set()
            for i in current_set:
                if i == k:
                    continue
                x_i, y_i = balls[i]
                
                # Remove if (X_i < X_k AND Y_i < Y_k) OR (X_i > X_k AND Y_i > Y_k)
                if (x_i < x_k and y_i < y_k) or (x_i > x_k and y_i > y_k):
                    removed.add(i)
            
            # The remaining set after this operation
            next_set = frozenset(current_set - removed)
            
            if next_set not in visited:
                visited.add(next_set)
                queue.append(next_set)
    
    print(len(visited) % MOD)

solve()
