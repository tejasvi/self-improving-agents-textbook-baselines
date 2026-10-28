def solve():
    T = input().strip()
    N = int(input().strip())
    
    bags = []
    for _ in range(N):
        line = input().strip().split()
        A = int(line[0])
        strings = line[1:A+1]
        bags.append(strings)
    
    # dp[i][j] = minimum cost to construct T[0:j] using bags 0 to i-1
    # Initialize with infinity
    INF = float('inf')
    dp = [[INF] * (len(T) + 1) for _ in range(N + 1)]
    
    # Base case: empty string requires 0 cost
    dp[0][0] = 0
    
    # For each bag
    for i in range(N):
        bag = bags[i]
        
        # For each position in T
        for j in range(len(T) + 1):
            # Option 1: Don't take anything from bag i
            dp[i+1][j] = min(dp[i+1][j], dp[i][j])
            
            # Option 2: Try to take each string from bag i
            # If we use string s from bag i, we need to have already constructed T[0:j]
            # where j is some position, and s matches T[j:j+len(s)]
            for s in bag:
                # For all positions k where we could have started using string s
                for k in range(len(T) + 1):
                    if k + len(s) <= len(T) and T[k:k+len(s)] == s:
                        # We can go from position k to position k+len(s) using string s
                        if dp[i][k] != INF:
                            dp[i+1][k+len(s)] = min(dp[i+1][k+len(s)], dp[i][k] + 1)
    
    result = dp[N][len(T)]
    if result == INF:
        print(-1)
    else:
        print(result)

solve()
