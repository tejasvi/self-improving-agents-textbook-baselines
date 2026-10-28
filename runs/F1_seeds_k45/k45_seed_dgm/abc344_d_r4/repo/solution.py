# Write your solution here. Read from stdin, write to stdout.

def solve():
    # Read input
    T = input().strip()
    N = int(input().strip())
    
    bags = []
    for _ in range(N):
        line = input().strip().split()
        A_i = int(line[0])
        strings = line[1:A_i+1]
        bags.append(strings)
    
    target_len = len(T)
    
    # DP: dp[i][j] = minimum cost to match first j characters of T using first i bags
    # Initialize with infinity
    INF = float('inf')
    dp = [[INF] * (target_len + 1) for _ in range(N + 1)]
    
    # Base case: 0 bags, 0 characters matched costs 0
    dp[0][0] = 0
    
    # Fill DP table
    for i in range(1, N + 1):
        # For each position j in target string
        for j in range(target_len + 1):
            # Option 1: skip bag i
            dp[i][j] = min(dp[i][j], dp[i-1][j])
            
            # Option 2: use a string from bag i
            for string in bags[i-1]:
                str_len = len(string)
                # Check if we can match this string starting at position j
                if j + str_len <= target_len and T[j:j+str_len] == string:
                    # We can use this string
                    if dp[i-1][j] != INF:
                        dp[i][j + str_len] = min(dp[i][j + str_len], dp[i-1][j] + 1)
    
    # The answer is dp[N][target_len]
    result = dp[N][target_len]
    if result == INF:
        print(-1)
    else:
        print(result)

solve()
