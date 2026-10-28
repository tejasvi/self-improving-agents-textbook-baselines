import heapq

def solve():
    # Read input
    N, K, P = map(int, input().split())
    
    plans = []
    for _ in range(N):
        line = list(map(int, input().split()))
        cost = line[0]
        increases = line[1:]
        plans.append((cost, increases))
    
    # Use Dijkstra's algorithm to find minimum cost
    # State: tuple of parameter values (clamped at P for optimization)
    # We only care about values up to P, values ≥ P are treated as P
    
    initial_state = tuple([0] * K)
    target_state = tuple([P] * K)
    
    # Priority queue: (cost, state)
    pq = [(0, initial_state)]
    visited = {}  # state -> minimum cost to reach this state
    visited[initial_state] = 0
    
    while pq:
        cost, state = heapq.heappop(pq)
        
        # Check if we've reached the goal
        if all(state[i] >= P for i in range(K)):
            print(cost)
            return
        
        # Skip if we've already found a better path to this state
        if state in visited and visited[state] < cost:
            continue
        
        # Try adding each plan
        for plan_idx, (plan_cost, increases) in enumerate(plans):
            new_state_list = list(state)
            for j in range(K):
                new_state_list[j] += increases[j]
            
            # Clamp values at P for state representation (optimization)
            new_state_list = [min(val, P) for val in new_state_list]
            new_state = tuple(new_state_list)
            new_cost = cost + plan_cost
            
            # Only proceed if we found a better path to this state
            if new_state not in visited or visited[new_state] > new_cost:
                visited[new_state] = new_cost
                heapq.heappush(pq, (new_cost, new_state))
    
    # If we get here, the goal is unreachable
    print(-1)

solve()
