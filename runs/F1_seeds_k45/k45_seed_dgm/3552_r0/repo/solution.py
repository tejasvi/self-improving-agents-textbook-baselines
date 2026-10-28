class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        # Special case: n = 1
        if n == 1:
            # Find largest single digit divisible by k
            for i in range(9, 0, -1):
                if i % k == 0:
                    return str(i)
            return "0"  # shouldn't reach here given constraints
        
        # For n > 1, we construct palindromes
        # A palindrome is determined by its first half
        # For even n, first_half_len = n // 2
        # For odd n, first_half_len = (n + 1) // 2
        
        first_half_len = (n + 1) // 2
        
        # Start from the maximum first half and work down
        # Maximum first half for n digits
        max_first_half = int('9' * first_half_len)
        
        # We need to iterate from max down to min
        # Min for n digits: if we want no leading zero, min is 10...0
        if n == 1:
            min_first_half = 1
        else:
            min_first_half = 10 ** (first_half_len - 1)
        
        # Try each possible first half from largest to smallest
        for first_half_val in range(max_first_half, min_first_half - 1, -1):
            first_half_str = str(first_half_val)
            
            # Create palindrome
            if n % 2 == 0:
                # Even length: mirror the entire first half
                palindrome_str = first_half_str + first_half_str[::-1]
            else:
                # Odd length: mirror all but the last digit of first half
                palindrome_str = first_half_str + first_half_str[-2::-1]
            
            # Check if divisible by k
            palindrome_num = int(palindrome_str)
            if palindrome_num % k == 0:
                return palindrome_str
        
        # If no palindrome found (shouldn't happen with valid input)
        return "0"
