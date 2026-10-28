def is_palindrome(s):
    """Check if string s is a palindrome"""
    return s == s[::-1]

def solve():
    MOD = 998244353
    
    n, k = map(int, input().split())
    s = input().strip()
    
    # Memoization for DP
    # Key: (index, last_k_minus_1_chars)
    memo = {}
    
    def backtrack(index, last_chars):
        """
        Recursively build strings and count valid ones.
        index: current position in s
        last_chars: the last (k-1) characters (or fewer if we haven't built k chars yet)
        """
        # Memoization key
        key = (index, last_chars)
        if key in memo:
            return memo[key]
        
        # Base case: we've processed all characters
        if index == n:
            return 1
        
        result = 0
        
        if s[index] == '?':
            # Try 'A'
            new_char = 'A'
            new_last_chars = (last_chars + new_char)[-(k-1):] if k > 1 else ''
            
            # Check if adding this character would create a palindrome of length k
            candidate = last_chars + new_char
            is_valid = True
            if len(candidate) >= k:
                if is_palindrome(candidate[-k:]):
                    is_valid = False
            
            if is_valid:
                result += backtrack(index + 1, new_last_chars)
                result %= MOD
            
            # Try 'B'
            new_char = 'B'
            new_last_chars = (last_chars + new_char)[-(k-1):] if k > 1 else ''
            
            # Check if adding this character would create a palindrome of length k
            candidate = last_chars + new_char
            is_valid = True
            if len(candidate) >= k:
                if is_palindrome(candidate[-k:]):
                    is_valid = False
            
            if is_valid:
                result += backtrack(index + 1, new_last_chars)
                result %= MOD
        else:
            # Character is fixed
            new_char = s[index]
            new_last_chars = (last_chars + new_char)[-(k-1):] if k > 1 else ''
            
            # Check if adding this character would create a palindrome of length k
            candidate = last_chars + new_char
            is_valid = True
            if len(candidate) >= k:
                if is_palindrome(candidate[-k:]):
                    is_valid = False
            
            if is_valid:
                result = backtrack(index + 1, new_last_chars)
        
        memo[key] = result
        return result
    
    return backtrack(0, '')

print(solve())
