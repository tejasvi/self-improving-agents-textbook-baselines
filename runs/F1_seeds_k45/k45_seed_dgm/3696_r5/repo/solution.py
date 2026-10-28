class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Count substrings of s that are divisible by their non-zero last digit.
        
        Approach:
        - For each ending position (j), consider all possible starting positions (i)
        - For each substring s[i:j+1], check if int(s[i:j+1]) % int(s[j]) == 0
        - Use modular arithmetic to efficiently compute the value modulo the last digit
        - For substring ending at j with last digit d, as we go backward from j-1 to 0,
          we can compute the modulo incrementally
        """
        count = 0
        n = len(s)
        
        # For each ending position
        for j in range(n):
            last_digit = int(s[j])
            
            # Skip if last digit is 0 (can't divide by 0)
            if last_digit == 0:
                continue
            
            # For substrings ending at position j, check all starting positions
            # We'll go backwards from j to 0, computing modulo incrementally
            current_mod = 0
            for i in range(j, -1, -1):
                digit = int(s[i])
                # Build the number from right to left (in terms of modulo)
                # If we have a number with mod value m, and we add digit d to the left,
                # the new number is d * 10^(j-i) + original_number
                # But we need to think about this differently:
                # current_mod represents the value of s[i:j+1] mod last_digit
                current_mod = (digit * pow(10, j - i, last_digit) + current_mod) % last_digit
                
                # Check if the substring s[i:j+1] is divisible by last_digit
                if current_mod == 0:
                    count += 1
        
        return count
