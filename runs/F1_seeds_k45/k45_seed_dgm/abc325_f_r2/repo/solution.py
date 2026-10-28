def solve():
    # Read input
    N = int(input())
    D = list(map(int, input().split()))
    L1, C1, K1 = map(int, input().split())
    L2, C2, K2 = map(int, input().split())
    
    # For each section, find all valid ways to cover it (x sensors of type 1, y sensors of type 2)
    # and their costs
    section_options = []
    
    for i in range(N):
        d = D[i]
        options = []  # List of (cost, x1, x2) tuples for this section
        
        # Try all combinations of sensors
        for x1 in range(K1 + 1):
            for x2 in range(K2 + 1):
                if x1 * L1 + x2 * L2 >= d:
                    cost = x1 * C1 + x2 * C2
                    options.append((cost, x1, x2))
        
        if not options:
            print(-1)
            return
        
        # Sort by cost and keep only the best ones
        options.sort()
        section_options.append(options)
    
    # Now we need to select one option for each section such that:
    # - Total x1 usage <= K1
    # - Total x2 usage <= K2
    # - Total cost is minimized
    
    # Use DP: dp[i][j][k] = minimum cost to cover first i sections using j type-1 sensors and k type-2 sensors
    INF = float('inf')
    dp = [[[INF for _ in range(K2 + 1)] for _ in range(K1 + 1)] for _ in range(N + 1)]
    dp[0][0][0] = 0
    
    for i in range(N):
        for j in range(K1 + 1):
            for k in range(K2 + 1):
                if dp[i][j][k] == INF:
                    continue
                
                # Try each option for section i
                for cost, x1, x2 in section_options[i]:
                    new_j = j + x1
                    new_k = k + x2
                    if new_j <= K1 and new_k <= K2:
                        dp[i + 1][new_j][new_k] = min(dp[i + 1][new_j][new_k], dp[i][j][k] + cost)
    
    # Find minimum cost
    result = INF
    for j in range(K1 + 1):
        for k in range(K2 + 1):
            result = min(result, dp[N][j][k])
    
    if result == INF:
        print(-1)
    else:
        print(result)

solve()
