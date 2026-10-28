# Write your solution here. Read from stdin, write to stdout.

def is_palindrome(s):
    """Check if a string is a palindrome"""
    return s == s[::-1]

def solve():
    MOD = 998244353
    N, K = map(int, input().split())
    S = input().strip()
    
    # DP approach: dp[i][suffix] = number of ways to fill positions 0..i-1
    # where suffix is the last K-1 characters
    # We use memoization with a dictionary
    
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(pos, suffix):
        """
        pos: current position in string S
        suffix: the last K-1 characters as a string
        Returns: number of valid ways to fill from pos to end
        """
        # Base case: we've filled all positions
        if pos == N:
            return 1
        
        result = 0
        
        # Determine what characters we can try at this position
        if S[pos] == '?':
            choices = ['A', 'B']
        else:
            choices = [S[pos]]
        
        for char in choices:
            # Create the new suffix (last K-1 characters including current)
            new_suffix = (suffix + char)[-K+1:] if K > 1 else ""
            
            # Check if adding this character creates a K-length palindrome
            if len(suffix) == K - 1:
                # We have K characters now: suffix + char
                candidate = suffix + char
                if is_palindrome(candidate):
                    # This would create a palindrome, skip it
                    continue
            
            # Recurse
            result = (result + dp(pos + 1, new_suffix)) % MOD
        
        return result
    
    # Start DP from position 0 with empty suffix
    answer = dp(0, "")
    print(answer)

solve()
