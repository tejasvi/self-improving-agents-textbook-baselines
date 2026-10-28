class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Count the number of substrings divisible by their non-zero last digit.
        
        Approach:
        - For each position j (ending position), we iterate through all possible starting positions i
        - We compute the substring value modulo the last digit using modular arithmetic
        - We don't need to convert the entire substring to integer, just track the remainder
        
        Time Complexity: O(n^2) where n is length of string
        Space Complexity: O(1)
        """
        count = 0
        n = len(s)
        
        # For each ending position
        for j in range(n):
            last_digit = int(s[j])
            
            # If last digit is 0, skip (problem says non-zero last digit)
            if last_digit == 0:
                continue
            
            # For each starting position
            remainder = 0
            for i in range(j, -1, -1):
                # Build the remainder by prepending the digit at position i
                digit = int(s[i])
                # remainder represents the value from i to j
                remainder = digit * pow(10, j - i, last_digit) + remainder
                remainder %= last_digit
                
                # Check if substring from i to j is divisible by last_digit
                if remainder == 0:
                    count += 1
        
        return count
