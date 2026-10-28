# Write your solution here. Read from stdin, write to stdout.

def solve():
    N = int(input())
    D = list(map(int, input().split()))
    L1, C1, K1 = map(int, input().split())
    L2, C2, K2 = map(int, input().split())
    
    # For each section, find the minimum cost to cover it with different combinations
    # of sensors (x1, x2) where x1 * L1 + x2 * L2 >= D_i
    
    # dp[i][j][k] = minimum cost to monitor first i sections using j type-1 sensors and k type-2 sensors
    # Initialize with infinity
    INF = float('inf')
    dp = [[[INF] * (K2 + 1) for _ in range(K1 + 1)] for _ in range(N + 1)]
    dp[0][0][0] = 0
    
    for i in range(N):
        # For section i, we need to cover D[i] meters
        # Try all combinations of sensors
        for used1 in range(K1 + 1):
            for used2 in range(K2 + 1):
                if dp[i][used1][used2] == INF:
                    continue
                
                # Try different combinations of new sensors for this section
                for add1 in range(K1 - used1 + 1):
                    for add2 in range(K2 - used2 + 1):
                        # Check if add1 type-1 and add2 type-2 sensors can cover D[i]
                        coverage = add1 * L1 + add2 * L2
                        if coverage >= D[i]:
                            new_used1 = used1 + add1
                            new_used2 = used2 + add2
                            new_cost = dp[i][used1][used2] + add1 * C1 + add2 * C2
                            dp[i + 1][new_used1][new_used2] = min(dp[i + 1][new_used1][new_used2], new_cost)
    
    # Find minimum cost across all valid final states
    min_cost = INF
    for j in range(K1 + 1):
        for k in range(K2 + 1):
            min_cost = min(min_cost, dp[N][j][k])
    
    if min_cost == INF:
        print(-1)
    else:
        print(min_cost)

solve()
