def solve():
    # Read input
    N, K, P = map(int, input().split())
    
    plans = []
    for _ in range(N):
        line = list(map(int, input().split()))
        cost = line[0]
        effects = tuple(line[1:K+1])
        plans.append((cost, effects))
    
    # DP approach: dp[state] = minimum cost to achieve state
    # where state is a tuple of parameter values (capped at P)
    # We iterate through each plan and update the DP table
    
    # Initially, we can only be in state (0, 0, ..., 0) with cost 0
    dp = {tuple([0] * K): 0}
    
    # For each plan, we update the DP table
    for plan_idx in range(N):
        plan_cost, effects = plans[plan_idx]
        
        # Create a new DP table for this iteration
        new_dp = dict(dp)  # Copy the current DP table
        
        # For each current state, try adding this plan
        for state, cost in dp.items():
            # Calculate new state after applying this plan
            new_state = tuple(min(state[i] + effects[i], P) for i in range(K))
            
            # Update the DP table if this is a better way to reach new_state
            new_cost = cost + plan_cost
            if new_state not in new_dp or new_dp[new_state] > new_cost:
                new_dp[new_state] = new_cost
        
        dp = new_dp
    
    # Find the minimum cost to reach the goal state
    goal_state = tuple([P] * K)
    min_cost = float('inf')
    
    for state, cost in dp.items():
        if all(param >= P for param in state):
            min_cost = min(min_cost, cost)
    
    if min_cost == float('inf'):
        return -1
    else:
        return min_cost

print(solve())
