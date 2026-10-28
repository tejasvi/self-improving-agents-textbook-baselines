class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        # Handle the case where n = 1
        if n == 1:
            # Find the largest single digit divisible by k
            for digit in range(9, 0, -1):
                if digit % k == 0:
                    return str(digit)
            return "0"
        
        # For n >= 2, we need to construct palindromes
        # The first half length is (n + 1) // 2
        # The second half length is n // 2
        first_half_len = (n + 1) // 2
        
        # Start with the largest possible first half
        # For first_half_len digits, the max is 10^first_half_len - 1
        # But we need to avoid leading zeros, so start from 10^(first_half_len - 1) - 1
        max_first_half = 10 ** first_half_len - 1
        min_first_half = 10 ** (first_half_len - 1)
        
        # Try each possible first half from largest to smallest
        for first_half in range(max_first_half, min_first_half - 1, -1):
            # Construct the palindrome
            first_half_str = str(first_half)
            
            # For even n: mirror the entire first half
            # For odd n: mirror all but the last digit
            if n % 2 == 0:
                # Even length palindrome: mirror entire first half
                palindrome_str = first_half_str + first_half_str[::-1]
            else:
                # Odd length palindrome: mirror all but last digit of first half
                palindrome_str = first_half_str + first_half_str[-2::-1]
            
            # Convert to integer and check divisibility
            palindrome_num = int(palindrome_str)
            if palindrome_num % k == 0:
                return palindrome_str
        
        # Should never reach here for valid inputs
        return ""
