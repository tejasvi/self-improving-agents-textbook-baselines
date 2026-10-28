class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Count the number of substrings divisible by their non-zero last digit.
        
        Approach:
        - For each ending position j in the string
        - For each starting position i <= j
        - Check if substring s[i:j+1] is divisible by int(s[j])
        
        To optimize: Use modular arithmetic. When computing substring values
        from right to left, we can track the modulo value as we extend left.
        
        For a digit d at position j (the last digit of our substring):
        - If d == 0, skip (can't divide by 0)
        - For substrings ending at j: track the numeric value mod d
        - When extending left by a digit c, new_value = c * 10^k + old_value
        - So new_mod = (c * 10^k + old_value) % d
        """
        count = 0
        n = len(s)
        
        # For each ending position
        for j in range(n):
            last_digit = int(s[j])
            
            # If last digit is 0, no substring ending here can be divisible by 0
            if last_digit == 0:
                continue
            
            # Track the value of substring modulo last_digit
            # We build from right to left (from position j going backwards)
            value_mod = 0
            power = 1  # This tracks 10^k mod last_digit where k is distance from j
            
            # For each starting position (going backwards from j)
            for i in range(j, -1, -1):
                digit = int(s[i])
                # Add this digit to the left of our current number
                value_mod = (digit * power + value_mod) % last_digit
                
                # Check if divisible
                if value_mod == 0:
                    count += 1
                
                # Update power for next iteration (next digit to the left)
                power = (power * 10) % last_digit
        
        return count
