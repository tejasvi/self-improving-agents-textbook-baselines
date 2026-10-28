def is_palindrome(s):
    """Check if string is a palindrome"""
    return s == s[::-1]

def solve():
    MOD = 998244353
    
    # Read input
    N, K = map(int, input().split())
    S = input().strip()
    
    # dp[i][suffix] = number of ways to fill first i characters 
    # where suffix is the last K-1 characters
    # suffix is represented as a tuple of characters
    
    dp = {}
    
    def get_valid_chars(pos):
        """Get which characters are valid at position pos"""
        if S[pos] == '?':
            return ['A', 'B']
        else:
            return [S[pos]]
    
    # Initialize: process first character
    for c in get_valid_chars(0):
        # The suffix after position 0 is just the character itself (or empty)
        suffix = (c,) if K > 1 else ()
        dp[suffix] = dp.get(suffix, 0) + 1
    
    # Process remaining characters
    for i in range(1, N):
        new_dp = {}
        
        for suffix, count in dp.items():
            # suffix contains last min(i, K-1) characters
            current_len = len(suffix)
            
            for c in get_valid_chars(i):
                # Build the new suffix (last K-1 chars after adding c)
                # First, try building a string to check if it forms a palindrome
                
                if current_len == K - 1:
                    # We have K-1 characters in suffix, adding one more gives K
                    test_string = ''.join(suffix) + c
                    if is_palindrome(test_string):
                        # This would create a palindrome, skip
                        continue
                    # New suffix: last K-1 chars of (suffix + c)
                    new_suffix = suffix[1:] + (c,)
                else:
                    # We don't have K-1 chars yet, just extend
                    new_suffix = suffix + (c,)
                
                new_dp[new_suffix] = (new_dp.get(new_suffix, 0) + count) % MOD
        
        dp = new_dp
    
    # Sum all valid endings
    result = sum(dp.values()) % MOD
    print(result)

solve()
