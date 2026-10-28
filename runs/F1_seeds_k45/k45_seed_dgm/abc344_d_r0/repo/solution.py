# Write your solution here. Read from stdin, write to stdout.

def solve():
    T = input().strip()
    N = int(input().strip())
    
    bags = []
    for _ in range(N):
        line = input().strip().split()
        A = int(line[0])
        strings = line[1:A+1]
        bags.append(strings)
    
    # DP approach: dp[i][j] = minimum cost to build T[0:j] using bags 0 to i-1
    # If impossible, dp[i][j] = float('inf')
    INF = float('inf')
    
    # dp[i][j] represents the state after processing bag i and building prefix T[0:j]
    dp = [[INF] * (len(T) + 1) for _ in range(N + 1)]
    dp[0][0] = 0  # Initially, we have processed 0 bags and built empty string with cost 0
    
    for i in range(N):
        for j in range(len(T) + 1):
            if dp[i][j] == INF:
                continue
            
            # Option 1: Do nothing with bag i
            dp[i+1][j] = min(dp[i+1][j], dp[i][j])
            
            # Option 2: Take one string from bag i
            for s in bags[i]:
                # Check if we can append s to T[0:j] to get T[0:j+len(s)]
                if j + len(s) <= len(T):
                    # Check if T[j:j+len(s)] == s
                    if T[j:j+len(s)] == s:
                        dp[i+1][j+len(s)] = min(dp[i+1][j+len(s)], dp[i][j] + 1)
    
    result = dp[N][len(T)]
    if result == INF:
        print(-1)
    else:
        print(result)

solve()
