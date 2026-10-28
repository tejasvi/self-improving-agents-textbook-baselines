import heapq

def solve():
    N, K, P = map(int, input().split())
    
    plans = []
    for _ in range(N):
        line = list(map(int, input().split()))
        cost = line[0]
        increases = line[1:]
        plans.append((cost, increases))
    
    # State: (parameter_tuple, frozenset_of_used_indices)
    # Use Dijkstra's algorithm to find minimum cost
    
    # Initial state: all parameters are 0, no plans used
    initial_state = (tuple([0] * K), frozenset())
    
    # visited: set of visited states
    visited = set()
    
    # Priority queue: (cost, state)
    pq = [(0, initial_state)]
    
    while pq:
        current_cost, state = heapq.heappop(pq)
        
        params, used_plans = state
        
        # Skip if already visited
        if state in visited:
            continue
        visited.add(state)
        
        # Check if we've reached the goal
        if all(params[i] >= P for i in range(K)):
            print(current_cost)
            return
        
        # Try executing each unused plan
        for i in range(N):
            if i in used_plans:
                continue  # Plan already used
            
            cost, increases = plans[i]
            
            # Calculate new parameter values
            new_params_list = list(params)
            for j in range(K):
                new_params_list[j] = min(new_params_list[j] + increases[j], P)
            new_params = tuple(new_params_list)
            
            new_cost = current_cost + cost
            new_used = used_plans | {i}
            new_state = (new_params, frozenset(new_used))
            
            # Only add if not visited
            if new_state not in visited:
                heapq.heappush(pq, (new_cost, new_state))
    
    # If we exit the loop without finding goal, it's impossible
    print(-1)

solve()
