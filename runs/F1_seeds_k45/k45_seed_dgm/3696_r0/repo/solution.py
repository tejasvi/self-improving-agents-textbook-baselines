class Solution:
    def countSubstrings(self, s: str) -> int:
        count = 0
        n = len(s)
        
        # For each position i as the last digit of a substring
        for i in range(n):
            last_digit = int(s[i])
            
            # Skip if last digit is 0 (can't divide by 0)
            if last_digit == 0:
                continue
            
            # Build substrings ending at i, moving backwards
            # remainder will track the number formed from j to i, mod last_digit
            remainder = 0
            power = 1
            
            # j goes from i down to 0
            for j in range(i, -1, -1):
                digit = int(s[j])
                # Add this digit to the left of our current number
                remainder = (digit * power + remainder) % last_digit
                power = (power * 10) % last_digit
                
                # Check if remainder is 0
                if remainder == 0:
                    count += 1
        
        return count
