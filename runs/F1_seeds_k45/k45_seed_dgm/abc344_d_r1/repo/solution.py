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
    
    target_len = len(T)
    
    # dp[i][j] = minimum cost to reach position j in T after processing first i bags
    # -1 means unreachable
    INF = float('inf')
    dp = [[INF] * (target_len + 1) for _ in range(N + 1)]
    dp[0][0] = 0  # Initially at position 0 with cost 0
    
    # Process each bag
    for i in range(N):
        for j in range(target_len + 1):
            if dp[i][j] == INF:
                continue  # Position j is not reachable after i bags
            
            # Option 1: Do nothing - stay at position j
            dp[i+1][j] = min(dp[i+1][j], dp[i][j])
            
            # Option 2: Try each string in bag i
            for s in bags[i]:
                # Check if string s matches T[j:j+len(s)]
                if j + len(s) <= target_len and T[j:j+len(s)] == s:
                    new_pos = j + len(s)
                    dp[i+1][new_pos] = min(dp[i+1][new_pos], dp[i][j] + 1)
    
    # The answer is the minimum cost to reach position target_len
    if dp[N][target_len] == INF:
        print(-1)
    else:
        print(dp[N][target_len])

solve()
