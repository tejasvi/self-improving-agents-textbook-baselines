from collections import deque

def solve():
    N, M = map(int, input().split())
    operations = []
    for _ in range(M):
        L, R = map(int, input().split())
        operations.append((L - 1, R - 1))  # Convert to 0-indexed
    
    # BFS to find minimum cost
    # State: (operation_index, tuple of positions that are 1)
    initial_state = (0, ())
    queue = deque([initial_state])
    visited = {initial_state: (0, [])}  # cost and path
    
    goal_set = set(range(N))
    
    while queue:
        op_idx, ones_tuple = queue.popleft()
        cost, path = visited[(op_idx, ones_tuple)]
        ones = set(ones_tuple)
        
        if op_idx == M:
            # Check if all positions are 1
            if ones == goal_set:
                print(cost)
                print(' '.join(map(str, path)))
            return
        
        L, R = operations[op_idx]
        
        # Try all three operations
        for op in range(3):
            if op == 0:
                # Do nothing
                new_ones = ones
                new_cost = cost
            elif op == 1:
                # Set [L, R] to 1
                new_ones = ones | set(range(L, R + 1))
                new_cost = cost + 1
            else:  # op == 2
                # Set outside [L, R] to 1
                new_ones = ones | set(i for i in range(N) if i < L or i > R)
                new_cost = cost + 1
            
            new_ones_tuple = tuple(sorted(new_ones))
            next_state = (op_idx + 1, new_ones_tuple)
            
            # Only add if not visited or if we found a cheaper path
            if next_state not in visited or visited[next_state][0] > new_cost:
                visited[next_state] = (new_cost, path + [op])
                queue.append(next_state)
    
    print(-1)

solve()
