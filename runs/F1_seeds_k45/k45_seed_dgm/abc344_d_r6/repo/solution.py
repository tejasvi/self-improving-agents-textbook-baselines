def solve():
    T = input().strip()
    N = int(input().strip())
    
    bags = []
    for _ in range(N):
        line = input().strip().split()
        A = int(line[0])
        strings = line[1:A+1]
        bags.append(strings)
    
    target_len = len(T)
    
    # dp[i][j] = minimum cost to process bags 0..i-1 and match first j characters of T
    # Initialize with infinity
    INF = float('inf')
    dp = [[INF] * (target_len + 1) for _ in range(N + 1)]
    
    # Base case: before processing any bag, we have matched 0 characters with cost 0
    dp[0][0] = 0
    
    # Process each bag
    for i in range(N):
        for j in range(target_len + 1):
            if dp[i][j] == INF:
                continue
            
            # Option 1: Do nothing (skip this bag)
            dp[i+1][j] = min(dp[i+1][j], dp[i][j])
            
            # Option 2: Select a string from bag i
            for string in bags[i]:
                string_len = len(string)
                # Check if we can append this string to match more of T
                if j + string_len <= target_len:
                    # Check if the string matches the next part of T
                    if T[j:j+string_len] == string:
                        dp[i+1][j+string_len] = min(dp[i+1][j+string_len], dp[i][j] + 1)
    
    # The answer is dp[N][target_len]
    result = dp[N][target_len]
    if result == INF:
        print(-1)
    else:
        print(result)

solve()
