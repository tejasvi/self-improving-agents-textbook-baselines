def is_palindrome(s):
    """Check if a string is a palindrome"""
    return s == s[::-1]

def solve():
    N, K = map(int, input().split())
    S = input().strip()
    
    MOD = 998244353
    
    # dp[i][last_k_minus_1] = number of ways to fill first i characters
    # where last_k_minus_1 is the tuple of last K-1 characters
    
    # Initialize DP
    dp = [dict() for _ in range(N + 1)]
    dp[0][tuple()] = 1
    
    for i in range(N):
        for state, count in dp[i].items():
            # Determine what characters we can place at position i
            candidates = []
            if S[i] == '?':
                candidates = ['A', 'B']
            else:
                candidates = [S[i]]
            
            for char in candidates:
                # Create new state: last K-1 characters
                new_state = list(state) + [char]
                
                # Check if we create a palindrome of length K
                is_valid = True
                if len(new_state) >= K:
                    substring = ''.join(new_state[-K:])
                    if is_palindrome(substring):
                        is_valid = False
                
                if is_valid:
                    # Keep only last K-1 characters
                    next_state = tuple(new_state[-(K-1):]) if len(new_state) >= K-1 else tuple(new_state)
                    
                    if next_state not in dp[i + 1]:
                        dp[i + 1][next_state] = 0
                    dp[i + 1][next_state] = (dp[i + 1][next_state] + count) % MOD
    
    # Sum all valid final states
    result = sum(dp[N].values()) % MOD
    print(result)

solve()
