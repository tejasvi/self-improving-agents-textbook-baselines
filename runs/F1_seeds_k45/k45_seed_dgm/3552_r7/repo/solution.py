class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        """
        Find the largest n-digit palindrome divisible by k.
        
        Strategy:
        1. For a palindrome with n digits, we only need to determine the first ceil(n/2) digits
        2. Mirror these digits to get the remaining digits
        3. Start from the largest possible palindrome and iterate downward
        4. Check divisibility by k for each palindrome
        5. Return the first (largest) one that is divisible by k
        """
        
        # Special case: if n == 1, just check digits 9 down to 1
        if n == 1:
            for digit in range(9, 0, -1):
                if digit % k == 0:
                    return str(digit)
            return ""
        
        # For n > 1, we need to construct palindromes
        # The first half has length ceil(n/2)
        half_len = (n + 1) // 2
        
        # Start with the maximum first half (all 9s)
        # We represent it as an integer for easier manipulation
        max_half = 10 ** half_len - 1  # e.g., for half_len=2, max_half=99
        
        # Iterate from max_half down to 10^(half_len-1) (to ensure no leading zeros for the full palindrome)
        min_half = 10 ** (half_len - 1)  # e.g., for half_len=2, min_half=10
        
        for half in range(max_half, min_half - 1, -1):
            # Build the palindrome
            half_str = str(half)
            
            if n % 2 == 0:
                # Even length: mirror the entire half
                palindrome_str = half_str + half_str[::-1]
            else:
                # Odd length: mirror everything except the middle digit
                palindrome_str = half_str + half_str[-2::-1]
            
            # Convert to integer and check divisibility
            palindrome_num = int(palindrome_str)
            if palindrome_num % k == 0:
                return palindrome_str
        
        # Should never reach here given valid constraints
        return ""
