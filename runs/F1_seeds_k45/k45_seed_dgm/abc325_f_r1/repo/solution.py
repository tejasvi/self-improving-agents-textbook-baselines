def solve():
    N = int(input())
    D = list(map(int, input().split()))
    
    L1, C1, K1 = map(int, input().split())
    L2, C2, K2 = map(int, input().split())
    
    # For each section, calculate all possible ways to cover it
    possible_ways = []
    
    for i in range(N):
        length = D[i]
        ways = []
        
        # Try all combinations of sensors for this section
        # Maximum we'd need is ceil(length / min(L1, L2)) of each type
        max_possible = (length + min(L1, L2) - 1) // min(L1, L2)
        max_type1 = min(K1, max_possible)
        max_type2 = min(K2, max_possible)
        
        # We need to cover the section
        for a in range(max_type1 + 1):
            for b in range(max_type2 + 1):
                # Check if a sensors of type 1 and b sensors of type 2 can cover length
                covered = a * L1 + b * L2
                if covered >= length:
                    cost = a * C1 + b * C2
                    ways.append((a, b, cost))
        
        if not ways:
            print(-1)
            return
        
        possible_ways.append(ways)
    
    # Use DP: dp[(k1, k2)] = minimum cost using sensors such that we've used k1 type1 and k2 type2
    # We use a dictionary to only store reachable states
    dp = {}
    dp[(0, 0)] = 0
    
    for i in range(N):
        new_dp = {}
        
        for (used_k1, used_k2), cost in dp.items():
            # Try each way to cover section i
            for a, b, way_cost in possible_ways[i]:
                new_k1 = used_k1 + a
                new_k2 = used_k2 + b
                
                if new_k1 <= K1 and new_k2 <= K2:
                    new_cost = cost + way_cost
                    key = (new_k1, new_k2)
                    
                    if key not in new_dp or new_dp[key] > new_cost:
                        new_dp[key] = new_cost
        
        dp = new_dp
        
        if not dp:
            print(-1)
            return
    
    # Find the answer: minimum cost overall
    if not dp:
        print(-1)
    else:
        min_cost = min(dp.values())
        print(min_cost)

solve()
