def solve():
    N = int(input())
    D = list(map(int, input().split()))
    
    # Read sensor info
    line1 = list(map(int, input().split()))
    L1, C1, K1 = line1[0], line1[1], line1[2]
    
    line2 = list(map(int, input().split()))
    L2, C2, K2 = line2[0], line2[1], line2[2]
    
    # For each section, find Pareto-optimal combinations
    # A combination (c1, c2) is Pareto-optimal if no other valid 
    # combination (c1', c2') uses fewer or equal sensors with lower cost
    section_combos = []
    
    for section_len in D:
        # Find all valid (count1, count2) pairs sorted by cost
        valid = []
        for count1 in range(K1 + 1):
            for count2 in range(K2 + 1):
                if count1 * L1 + count2 * L2 >= section_len:
                    valid.append((count1, count2))
        
        if not valid:
            print(-1)
            return
        
        # Filter to keep only Pareto-optimal solutions
        # A solution (c1, c2) is Pareto-optimal if no other solution 
        # (c1', c2') has c1' <= c1 AND c2' <= c2 AND (c1', c2') != (c1, c2)
        pareto = []
        for c1, c2 in valid:
            dominated = False
            for c1p, c2p in valid:
                if c1p <= c1 and c2p <= c2 and (c1p != c1 or c2p != c2):
                    dominated = True
                    break
            if not dominated:
                pareto.append((c1, c2))
        
        section_combos.append(pareto)
    
    # DP: dp[j][k] = minimum cost to cover all sections using exactly j type-1 and k type-2 sensors
    INF = float('inf')
    dp = [[INF] * (K2 + 1) for _ in range(K1 + 1)]
    dp[0][0] = 0
    
    for i in range(N):
        # Process section i
        new_dp = [[INF] * (K2 + 1) for _ in range(K1 + 1)]
        
        for j in range(K1 + 1):
            for k in range(K2 + 1):
                if dp[j][k] == INF:
                    continue
                
                # Try all Pareto-optimal ways to cover section i
                for count1, count2 in section_combos[i]:
                    new_j = j + count1
                    new_k = k + count2
                    
                    if new_j <= K1 and new_k <= K2:
                        cost = count1 * C1 + count2 * C2
                        new_dp[new_j][new_k] = min(
                            new_dp[new_j][new_k],
                            dp[j][k] + cost
                        )
        
        dp = new_dp
    
    # Find minimum cost
    result = INF
    for j in range(K1 + 1):
        for k in range(K2 + 1):
            result = min(result, dp[j][k])
    
    if result == INF:
        print(-1)
    else:
        print(result)

solve()
