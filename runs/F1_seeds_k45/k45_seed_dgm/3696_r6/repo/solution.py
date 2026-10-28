class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Count the number of substrings of s divisible by their non-zero last digit.
        
        Approach:
        - For each ending position i, iterate through all starting positions j
        - For each substring s[j:i+1], check if it's divisible by s[i]
        - Use modular arithmetic to compute the value mod last_digit
        - Build the number from right to left using: (digit * power + remainder) % last_digit
        """
        count = 0
        n = len(s)
        
        # For each ending position
        for i in range(n):
            last_digit = int(s[i])
            
            # If last digit is 0, it can't divide anything (skip this ending position)
            if last_digit == 0:
                continue
            
            # For each starting position
            remainder = 0
            power = 1
            
            # Go backwards from position i to 0
            for j in range(i, -1, -1):
                digit = int(s[j])
                # Add this digit to our number: remainder represents the number mod last_digit
                remainder = (digit * power + remainder) % last_digit
                
                # Check if divisible by last_digit
                if remainder == 0:
                    count += 1
                
                # Update power for the next iteration (moving left)
                power = (power * 10) % last_digit
        
        return count
