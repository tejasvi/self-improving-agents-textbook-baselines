class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        # Special case: n = 1
        if n == 1:
            # Check single digits from 9 down to 1
            for digit in range(9, 0, -1):
                if digit % k == 0:
                    return str(digit)
            return "0"  # Should not reach here given constraints
        
        # For n >= 2
        # We need to construct a palindrome with n digits
        # A palindrome is determined by its first ceil(n/2) digits
        
        # Start with the largest possible palindrome
        half_len = (n + 1) // 2  # Length of the first half (including middle for odd n)
        
        # Start from the largest possible half: 10^half_len - 1 (e.g., 999 for half_len=3)
        # But ensure the first digit is not 0
        start = 10 ** half_len - 1
        
        # Iterate downward through possible halves
        for half_value in range(start, 10 ** (half_len - 1) - 1, -1):
            # Convert half to string
            half_str = str(half_value)
            
            # Create the full palindrome
            if n % 2 == 1:
                # Odd length: mirror the first (half_len - 1) digits
                palindrome_str = half_str + half_str[-2::-1]
            else:
                # Even length: mirror all digits of the half
                palindrome_str = half_str + half_str[::-1]
            
            # Convert to integer and check divisibility
            palindrome_int = int(palindrome_str)
            if palindrome_int % k == 0:
                return palindrome_str
        
        # If no palindrome found (shouldn't happen with valid inputs)
        return ""
