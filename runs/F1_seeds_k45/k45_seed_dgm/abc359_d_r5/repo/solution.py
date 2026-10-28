def is_palindrome(s):
    return s == s[::-1]

def solve():
    MOD = 998244353
    
    # Read input
    N, K = map(int, input().split())
    S = input().strip()
    
    # DP approach: dp[pos][last_k_minus_1] = number of ways
    # last_k_minus_1 is a tuple of the last K-1 characters
    
    # We'll use memoization with recursion
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(pos, last_chars):
        """
        pos: current position in string
        last_chars: tuple of last (K-1) characters we placed, or fewer if pos < K-1
        Returns: number of valid ways to fill from position pos onwards
        """
        
        if pos == N:
            # We've filled the entire string successfully
            return 1
        
        count = 0
        
        # Determine what characters we can place at position pos
        if S[pos] == '?':
            chars_to_try = ['A', 'B']
        else:
            chars_to_try = [S[pos]]
        
        for ch in chars_to_try:
            # Check if placing ch at position pos creates a palindrome of length K
            new_last_chars = last_chars + (ch,)
            
            # Check if the last K characters form a palindrome
            is_valid = True
            if len(new_last_chars) >= K:
                # Extract the last K characters (current substring of length K)
                last_k = new_last_chars[-K:]
                if is_palindrome(''.join(last_k)):
                    is_valid = False
            
            if is_valid:
                # Keep only the last K-1 characters for the next state
                next_last_chars = new_last_chars[-(K-1):] if len(new_last_chars) >= K-1 else new_last_chars
                count = (count + dp(pos + 1, next_last_chars)) % MOD
        
        return count
    
    # Start with empty last_chars
    result = dp(0, ())
    print(result)

solve()
