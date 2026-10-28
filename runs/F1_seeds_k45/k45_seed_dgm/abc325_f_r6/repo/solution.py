#!/usr/bin/env python3

def solve():
    N = int(input())
    D = list(map(int, input().split()))
    L1, C1, K1 = map(int, input().split())
    L2, C2, K2 = map(int, input().split())
    
    # For each section, calculate the minimum cost to monitor it
    # given different amounts of type-1 and type-2 sensors used
    
    # For a section of length d, we need a*L1 + b*L2 >= d
    # We want to minimize a*C1 + b*C2
    
    # DP approach: for each section, try all possible combinations
    # and track the minimum cost for using up to k1 type-1 sensors and k2 type-2 sensors
    
    # dp[i][j] = minimum cost to monitor first i sections using at most j type-1 and k type-2 sensors
    # But we need to track both sensor counts...
    
    # Better approach: for each section, precompute minimum cost for different sensor counts
    # Then use DP to select which allocation to use
    
    INF = float('inf')
    
    # For each section, compute: min_cost[section][k1_used][k2_used]
    # This is too memory intensive, so let's think differently
    
    # For each section, find all feasible (k1, k2) pairs and their costs
    min_costs = []
    for d in D:
        section_costs = {}  # (k1, k2) -> cost
        
        # Try all combinations of sensors for this section
        for k1 in range(K1 + 1):
            for k2 in range(K2 + 1):
                coverage = k1 * L1 + k2 * L2
                if coverage >= d:
                    cost = k1 * C1 + k2 * C2
                    key = (k1, k2)
                    if key not in section_costs or section_costs[key] > cost:
                        section_costs[key] = cost
        
        min_costs.append(section_costs)
    
    # Check if any section cannot be monitored
    for costs in min_costs:
        if not costs:
            print(-1)
            return
    
    # Now we need to select one (k1, k2) pair for each section
    # such that sum of k1 <= K1 and sum of k2 <= K2
    # and total cost is minimized
    
    # DP: dp[i][j][k] = minimum cost to monitor first i sections
    # using exactly j type-1 sensors and exactly k type-2 sensors
    
    dp = [[[INF] * (K2 + 1) for _ in range(K1 + 1)] for _ in range(N + 1)]
    dp[0][0][0] = 0
    
    for i in range(N):
        for j in range(K1 + 1):
            for k in range(K2 + 1):
                if dp[i][j][k] == INF:
                    continue
                
                # Try each feasible (k1, k2) combination for section i
                for (k1, k2), cost in min_costs[i].items():
                    new_j = j + k1
                    new_k = k + k2
                    if new_j <= K1 and new_k <= K2:
                        dp[i + 1][new_j][new_k] = min(
                            dp[i + 1][new_j][new_k],
                            dp[i][j][k] + cost
                        )
    
    # Find minimum cost across all valid (j, k) pairs
    result = INF
    for j in range(K1 + 1):
        for k in range(K2 + 1):
            result = min(result, dp[N][j][k])
    
    if result == INF:
        print(-1)
    else:
        print(result)

solve()
