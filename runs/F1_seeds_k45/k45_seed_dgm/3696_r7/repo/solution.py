class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Count the number of substrings divisible by their last digit.
        
        Approach:
        - For each ending position j, if s[j] is not '0', check all substrings ending at j
        - For efficiency, use modular arithmetic: compute the remainder as we go backwards
        - For substring from i to j, value % s[j] can be computed incrementally
        
        Key insight: When we add a digit to the left of a number:
        new_value = digit * 10^(length-1) + old_value
        new_value % last_digit = (digit * 10^(length-1) + old_value) % last_digit
        """
        count = 0
        n = len(s)
        
        for j in range(n):
            last_digit = int(s[j])
            
            # If last digit is 0, no substring ending here can be divisible by 0
            if last_digit == 0:
                continue
            
            # Check all substrings ending at position j
            remainder = 0
            power_of_10 = 1
            
            for i in range(j, -1, -1):
                digit = int(s[i])
                # Add digit to the left: remainder = digit * 10^(j-i) + remainder
                remainder = (digit * power_of_10 + remainder) % last_digit
                power_of_10 = (power_of_10 * 10) % last_digit
                
                if remainder == 0:
                    count += 1
        
        return count
