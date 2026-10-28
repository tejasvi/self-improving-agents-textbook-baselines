# Write your solution here. Read from stdin, write to stdout.

def solve():
    # Read input
    N, K, P = map(int, input().split())
    
    plans = []
    for _ in range(N):
        line = list(map(int, input().split()))
        cost = line[0]
        params = tuple(line[1:K+1])
        plans.append((cost, params))
    
    # DP: state is a tuple of K parameter values (capped at P for efficiency)
    # dp[state] = minimum cost to reach that state
    dp = {tuple([0] * K): 0}
    
    # Process each plan
    for cost, params in plans:
        new_dp = {}
        
        for state, state_cost in dp.items():
            # Option 1: Don't use this plan
            if state not in new_dp or new_dp[state] > state_cost:
                new_dp[state] = state_cost
            
            # Option 2: Use this plan
            new_state = tuple(min(state[i] + params[i], P) for i in range(K))
            new_cost = state_cost + cost
            
            if new_state not in new_dp or new_dp[new_state] > new_cost:
                new_dp[new_state] = new_cost
        
        dp = new_dp
    
    # Target state: all parameters at least P
    target = tuple([P] * K)
    
    if target in dp:
        print(dp[target])
    else:
        print(-1)

solve()
