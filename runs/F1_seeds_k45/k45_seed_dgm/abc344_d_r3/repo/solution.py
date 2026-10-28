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
    
    # dp[i][j] = minimum cost to match first j characters of T using bags 0..i-1
    # -1 means impossible
    INF = float('inf')
    dp = [[-1] * (target_len + 1) for _ in range(N + 1)]
    dp[0][0] = 0  # Before any bag, we've matched 0 characters with 0 cost
    
    # Process each bag
    for i in range(N):
        for j in range(target_len + 1):
            if dp[i][j] == -1:
                continue
            
            # Option 1: Do nothing with bag i
            if dp[i+1][j] == -1:
                dp[i+1][j] = dp[i][j]
            else:
                dp[i+1][j] = min(dp[i+1][j], dp[i][j])
            
            # Option 2: Pick a string from bag i
            for string in bags[i]:
                string_len = len(string)
                # Check if we can concatenate this string
                if j + string_len <= target_len:
                    # Check if the string matches the next characters in T
                    if T[j:j+string_len] == string:
                        new_pos = j + string_len
                        new_cost = dp[i][j] + 1
                        if dp[i+1][new_pos] == -1:
                            dp[i+1][new_pos] = new_cost
                        else:
                            dp[i+1][new_pos] = min(dp[i+1][new_pos], new_cost)
    
    result = dp[N][target_len]
    print(result)

solve()
