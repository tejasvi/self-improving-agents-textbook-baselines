class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        # Special case: n = 1
        if n == 1:
            # Find the largest single digit palindrome divisible by k
            for digit in range(9, -1, -1):
                if digit % k == 0:
                    return str(digit)
            return "0"
        
        # For n > 1, we need to construct a palindrome
        # The palindrome has n digits total
        # We need to fill the first ceil(n/2) digits
        
        # The first digit must be at least 1 (no leading zeros)
        # For the largest palindrome, start with first digit = 9 and work downwards
        
        half_len = (n + 1) // 2  # Length of the first half (including middle for odd n)
        
        # Generate palindrome by mirroring
        def make_palindrome(half_str):
            if n % 2 == 0:
                # Even length: mirror entire half
                return half_str + half_str[::-1]
            else:
                # Odd length: mirror all but the middle digit
                return half_str + half_str[-2::-1]
        
        # Start from the largest possible half and work downwards
        # For the first half, the first digit should be at least 1
        start = 10 ** half_len - 1  # Largest half_len digit number
        end = 10 ** (half_len - 1)  # Smallest half_len digit number (with leading 1)
        
        for half_val in range(start, end - 1, -1):
            half_str = str(half_val)
            palindrome_str = make_palindrome(half_str)
            palindrome_num = int(palindrome_str)
            
            if palindrome_num % k == 0:
                return palindrome_str
        
        return ""
