MOD = 998244353

def is_palindrome(s):
    """Check if a string is a palindrome."""
    return s == s[::-1]

def solve():
    # Read input
    N, K = map(int, input().split())
    S = input().strip()
    
    # DP with memoization
    # State: (position, last_K-1_chars as string)
    memo = {}
    
    def dp(pos, last_chars):
        """
        pos: current position in string (0 to N-1)
        last_chars: string of last K-1 characters (or fewer if pos < K-1)
        Returns: number of valid ways to fill positions [pos, N-1]
        """
        if pos == N:
            return 1
        
        # Create state for memoization
        state = (pos, last_chars)
        if state in memo:
            return memo[state]
        
        result = 0
        
        # Determine which characters we can place at position pos
        if S[pos] == '?':
            candidates = ['A', 'B']
        else:
            candidates = [S[pos]]
        
        for char in candidates:
            # Build the current substring (last K-1 chars + new char)
            current_substr = last_chars + char
            
            # Check if we have K characters to check for palindrome
            if len(current_substr) == K:
                # Check if current_substr is a palindrome
                if is_palindrome(current_substr):
                    # Skip this character as it creates a palindrome
                    continue
                # Keep only the last K-1 characters for next iteration
                next_last_chars = current_substr[1:]
            else:
                # Still building up to K characters
                next_last_chars = current_substr
            
            # Recursively fill the rest
            result = (result + dp(pos + 1, next_last_chars)) % MOD
        
        memo[state] = result
        return result
    
    answer = dp(0, "")
    print(answer)

solve()
