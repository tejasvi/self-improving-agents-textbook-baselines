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
    
    # dp[i][j] = minimum cost to build first j characters of T using bags 0..i-1
    # -1 means impossible
    INF = float('inf')
    dp = [[INF] * (target_len + 1) for _ in range(N + 1)]
    
    # Base case: 0 bags used, 0 characters matched
    dp[0][0] = 0
    
    # Fill DP table
    for i in range(N):  # For each bag
        for j in range(target_len + 1):  # For each position in target
            # Option 1: Don't take from bag i
            if dp[i][j] < INF:
                dp[i+1][j] = min(dp[i+1][j], dp[i][j])
            
            # Option 2: Take a string from bag i
            if dp[i][j] < INF:
                for string in bags[i]:
                    string_len = len(string)
                    new_pos = j + string_len
                    
                    # Check if this string matches the target at position j
                    if new_pos <= target_len and T[j:new_pos] == string:
                        dp[i+1][new_pos] = min(dp[i+1][new_pos], dp[i][j] + 1)
    
    result = dp[N][target_len]
    if result == INF:
        print(-1)
    else:
        print(result)

solve()
