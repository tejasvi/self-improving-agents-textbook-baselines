def solve():
    # Read input
    N = int(input())
    D = list(map(int, input().split()))
    
    L1, C1, K1 = map(int, input().split())
    L2, C2, K2 = map(int, input().split())
    
    # For each section, find all valid (x1, x2) pairs where:
    # x1 * L1 + x2 * L2 >= D_i
    # x1 <= K1, x2 <= K2
    
    # Get all valid ways to cover each section
    section_options = []
    for d in D:
        options = []  # List of (cost, x1, x2) for this section
        
        # Maximum type-1 sensors we might need (and can use)
        max_x1 = min(K1, (d + L1 - 1) // L1)
        
        # Try all combinations of type-1 and type-2 sensors
        for x1 in range(max_x1 + 1):
            # Remaining length after using x1 type-1 sensors
            remaining = d - x1 * L1
            if remaining <= 0:
                # x1 sensors of type-1 are enough
                x2 = 0
            else:
                # Need at least ceil(remaining / L2) type-2 sensors
                x2 = (remaining + L2 - 1) // L2
            
            if x2 <= K2:
                cost = x1 * C1 + x2 * C2
                options.append((cost, x1, x2))
        
        if not options:
            # This section cannot be covered
            print(-1)
            return
        
        section_options.append(options)
    
    # DP: use a dictionary to store only reachable states
    # State: (k1, k2) -> minimum cost
    INF = float('inf')
    dp = {(0, 0): 0}
    
    for i in range(N):
        new_dp = {}
        
        for (k1, k2), cost in dp.items():
            # Try each option for section i
            for opt_cost, x1, x2 in section_options[i]:
                new_k1 = k1 + x1
                new_k2 = k2 + x2
                
                if new_k1 <= K1 and new_k2 <= K2:
                    new_cost = cost + opt_cost
                    if (new_k1, new_k2) not in new_dp or new_dp[(new_k1, new_k2)] > new_cost:
                        new_dp[(new_k1, new_k2)] = new_cost
        
        dp = new_dp
    
    # Find the minimum cost to cover all sections
    if not dp:
        print(-1)
    else:
        result = min(dp.values())
        print(result)

solve()
