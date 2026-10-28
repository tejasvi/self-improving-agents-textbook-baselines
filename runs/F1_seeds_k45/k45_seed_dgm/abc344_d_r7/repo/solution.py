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
    
    # dp[i][j] = minimum cost to form T[0:j] using bags 0..i-1
    # Initialize with infinity
    INF = float('inf')
    dp = [[INF] * (len(T) + 1) for _ in range(N + 1)]
    
    # Base case: to form empty string, we need 0 cost
    for i in range(N + 1):
        dp[i][0] = 0
    
    # Process each bag
    for i in range(N):
        for j in range(len(T) + 1):
            # Option 1: Don't take anything from bag i
            dp[i + 1][j] = min(dp[i + 1][j], dp[i][j])
            
            # Option 2: Take a string from bag i (if it matches)
            if dp[i][j] < INF:
                for s in bags[i]:
                    # Check if we can append string s at position j
                    if j + len(s) <= len(T) and T[j:j+len(s)] == s:
                        new_pos = j + len(s)
                        dp[i + 1][new_pos] = min(dp[i + 1][new_pos], dp[i][j] + 1)
    
    result = dp[N][len(T)]
    if result == INF:
        print(-1)
    else:
        print(result)

solve()
