class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Count the number of substrings divisible by their last non-zero digit.
        
        Approach:
        - For each ending position j, we iterate backwards
        - We maintain the value of the substring modulo the last digit
        - For each position i to j, we check if the substring is divisible
          by the last digit (which is s[j])
        
        For efficiency:
        - We use modular arithmetic to avoid dealing with very large numbers
        - The remainder of substring s[i:j+1] when divided by s[j] can be
          computed incrementally as we go backwards
        """
        count = 0
        n = len(s)
        
        # For each ending position
        for j in range(n):
            last_digit = int(s[j])
            
            # If last digit is 0, skip (can't divide by 0)
            if last_digit == 0:
                continue
            
            # Build substrings ending at j, going backwards
            remainder = 0
            power_of_10 = 1
            
            for i in range(j, -1, -1):
                digit = int(s[i])
                # Update the remainder: new_remainder = digit * 10^(j-i) + remainder
                remainder = (digit * power_of_10 + remainder) % last_digit
                
                # Check if current substring s[i:j+1] is divisible by last_digit
                if remainder == 0:
                    count += 1
                
                # Update power of 10 for next iteration (going left)
                power_of_10 = (power_of_10 * 10) % last_digit
        
        return count
