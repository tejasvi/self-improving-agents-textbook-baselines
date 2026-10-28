class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Count the number of substrings divisible by their non-zero last digit.
        
        For each position i in the string (from right to left perspective),
        we iterate backwards to find all substrings ending at position i.
        For each substring, we check if it's divisible by its last digit (s[i]).
        
        Key insight: We can compute the remainder incrementally as we go backwards
        from each position, without needing to store the entire number.
        """
        n = len(s)
        count = 0
        
        # For each ending position i
        for i in range(n):
            last_digit = int(s[i])
            
            # Skip if last digit is 0 (can't divide by 0)
            if last_digit == 0:
                continue
            
            # Initialize remainder for substring ending at i
            remainder = 0
            
            # Iterate backwards from position i to find all substrings ending at i
            for j in range(i, -1, -1):
                # Add the digit at position j to our number (as we're building from right to left)
                digit = int(s[j])
                remainder = (digit * pow(10, i - j, last_digit) + remainder) % last_digit
                
                # Check if the substring from j to i is divisible by last_digit
                if remainder == 0:
                    count += 1
        
        return count
