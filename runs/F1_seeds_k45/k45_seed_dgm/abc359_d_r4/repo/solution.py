# Write your solution here. Read from stdin, write to stdout.

MOD = 998244353

def is_palindrome(s):
    """Check if a string is a palindrome"""
    return s == s[::-1]

def solve():
    # Read input
    N, K = map(int, input().split())
    S = input().strip()
    
    # DP approach: dp[suffix] = number of ways to reach this state
    # suffix contains the last K-1 characters
    # This ensures we can check if the last K characters form a palindrome
    
    # dp[suffix] = number of ways to fill characters such that
    # the last K-1 characters are 'suffix'
    dp = {}
    dp[""] = 1
    
    for i in range(N):
        new_dp = {}
        
        # Determine what characters we can place at position i
        if S[i] == '?':
            choices = ['A', 'B']
        else:
            choices = [S[i]]
        
        for suffix, count in dp.items():
            for char in choices:
                # Build the string of last K characters: suffix + char
                combined = suffix + char
                
                # Check if the last K characters form a palindrome
                valid = True
                if len(combined) >= K:
                    last_k = combined[-K:]
                    if is_palindrome(last_k):
                        valid = False
                
                if valid:
                    # Keep only the last K-1 characters for the next state
                    if len(combined) >= K:
                        new_suffix = combined[-(K-1):]
                    else:
                        new_suffix = combined
                    
                    if new_suffix not in new_dp:
                        new_dp[new_suffix] = 0
                    new_dp[new_suffix] = (new_dp[new_suffix] + count) % MOD
        
        dp = new_dp
    
    # Sum all valid configurations
    result = sum(dp.values()) % MOD
    print(result)

solve()
