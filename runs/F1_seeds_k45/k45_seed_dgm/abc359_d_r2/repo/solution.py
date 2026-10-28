def is_palindrome(s):
    """Check if a string is a palindrome"""
    return s == s[::-1]

def solve():
    MOD = 998244353
    
    # Read input
    N, K = map(int, input().split())
    S = input().strip()
    
    # DP with memoization
    # State: (position, last_k_minus_1_chars)
    # We track the last K-1 characters to determine what we can place next
    memo = {}
    
    def dp(pos, last_chars):
        """
        pos: current position in string
        last_chars: tuple of last min(K-1, pos) characters
        Returns: number of valid ways to fill the rest of the string
        """
        if pos == N:
            return 1
        
        state = (pos, last_chars)
        if state in memo:
            return memo[state]
        
        result = 0
        
        # Determine what characters we can place at position pos
        if S[pos] == '?':
            candidates = ['A', 'B']
        else:
            candidates = [S[pos]]
        
        for ch in candidates:
            # Check if placing ch at pos creates a palindrome of length K
            # The substring is: last_chars + ch
            if len(last_chars) == K - 1:
                substring = last_chars + (ch,)
                # Convert tuple to string for palindrome check
                substr_str = ''.join(substring)
                
                if not is_palindrome(substr_str):
                    # Update last_chars for next position
                    # Keep only the last K-1 characters
                    new_last_chars = last_chars[1:] + (ch,)
                    result = (result + dp(pos + 1, new_last_chars)) % MOD
            else:
                # We haven't reached K characters yet, so no palindrome check needed
                new_last_chars = last_chars + (ch,)
                result = (result + dp(pos + 1, new_last_chars)) % MOD
        
        memo[state] = result
        return result
    
    # Start DP from position 0 with empty last_chars
    answer = dp(0, ())
    print(answer)

solve()
