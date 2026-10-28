class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        """
        Find the largest n-digit palindrome divisible by k.
        
        Strategy using DFS with memoization:
        1. Build the palindrome by placing digits at symmetric positions
        2. For position i, place a digit that appears at both position i and position n-1-i
        3. For odd n, the middle digit appears only once
        4. Track the modulo remainder and use memoization
        """
        
        # Special case: n = 1
        if n == 1:
            # Check single digits from 9 down to 1 (no leading zeros)
            for digit in range(9, 0, -1):
                if digit % k == 0:
                    return str(digit)
            return ""
        
        # Precompute powers of 10 mod k for each position
        powers = [1] * n
        for i in range(1, n):
            powers[i] = (powers[i-1] * 10) % k
        
        memo = {}
        
        def dfs(pos, mod_val):
            """
            DFS to construct the palindrome by filling from position 0 onwards
            pos: current position to fill (0-indexed from left)
            mod_val: current modulo k value of the palindrome constructed so far
            Returns: (found, remaining_palindrome_string) or (False, "")
            """
            # We need to fill positions 0 to ceil(n/2)-1
            # Then mirror them
            half_len = (n + 1) // 2
            
            if pos == half_len:
                # We've filled the first half, check if mod is 0
                if mod_val == 0:
                    return (True, "")
                else:
                    return (False, "")
            
            state = (pos, mod_val)
            if state in memo:
                return memo[state]
            
            # Try digits from 9 down to 0 (or 1 for the first digit)
            start = 9
            
            for digit in range(start, -1, -1):
                # First digit can't be 0
                if pos == 0 and digit == 0:
                    continue
                
                # Calculate the contribution of this digit to the modulo
                # It appears at position pos and also at position n-1-pos (unless it's the middle digit of odd-length palindrome)
                
                mirror_pos = n - 1 - pos
                
                # Power of 10 at position pos (from left, so 10^(n-1-pos))
                power_left = powers[n - 1 - pos]
                
                # Power of 10 at mirror_pos (from left, so 10^(n-1-mirror_pos) = 10^pos)
                power_right = powers[n - 1 - mirror_pos]
                
                # Contribution to modulo
                if pos == mirror_pos:
                    # This is the middle digit of an odd-length palindrome, count only once
                    contrib = (digit * power_left) % k
                else:
                    # Count both positions
                    contrib = (digit * power_left + digit * power_right) % k
                
                new_mod = (mod_val + contrib) % k
                
                # Recursively try the next position
                found, rest = dfs(pos + 1, new_mod)
                if found:
                    result = str(digit) + rest
                    memo[state] = (True, result)
                    return (True, result)
            
            memo[state] = (False, "")
            return (False, "")
        
        found, first_half = dfs(0, 0)
        
        if not found:
            return ""
        
        # Build the complete palindrome from the first half
        if n % 2 == 0:
            # Even length: mirror the entire first half
            return first_half + first_half[::-1]
        else:
            # Odd length: the first half already includes the middle digit
            # Mirror only the part before the middle
            return first_half + first_half[-2::-1]
