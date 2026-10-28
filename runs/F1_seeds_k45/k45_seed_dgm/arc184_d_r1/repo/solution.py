from collections import deque

def solve():
    N = int(input())
    balls = []
    for i in range(N):
        x, y = map(int, input().split())
        balls.append((x, y, i))  # Store position and original index
    
    # BFS to find all reachable states
    initial_state = tuple(range(N))  # All balls present
    visited = set()
    queue = deque([initial_state])
    visited.add(initial_state)
    
    while queue:
        state = queue.popleft()
        
        # Try removing each ball in the current state
        for chosen_idx in state:
            x_k, y_k, _ = balls[chosen_idx]
            
            # Find which balls to remove
            new_state_list = []
            for idx in state:
                x_i, y_i, _ = balls[idx]
                
                # Check if ball i should be removed
                # Remove if (X_i < X_k and Y_i < Y_k) or (X_i > X_k and Y_i > Y_k)
                if (x_i < x_k and y_i < y_k) or (x_i > x_k and y_i > y_k):
                    # Remove this ball
                    pass
                else:
                    # Keep this ball
                    new_state_list.append(idx)
            
            new_state = tuple(sorted(new_state_list))
            
            if new_state not in visited:
                visited.add(new_state)
                queue.append(new_state)
    
    print(len(visited) % 998244353)

solve()
