class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        """
        Find the largest n-digit palindrome divisible by k.
        
        We iterate through possible first halves starting from the largest and
        working downward, checking if the resulting palindrome is divisible by k.
        """
        
        if n == 1:
            for digit in range(9, 0, -1):
                if digit % k == 0:
                    return str(digit)
            return ""
        
        half_len = (n + 1) // 2
        is_odd = n % 2 == 1
        
        def make_palindrome(half_str):
            if is_odd:
                return half_str + half_str[-2::-1]
            else:
                return half_str + half_str[::-1]
        
        # Try all first halves from largest to smallest
        max_half = 10 ** half_len - 1
        min_half = 10 ** (half_len - 1)
        
        for first_half_num in range(max_half, min_half - 1, -1):
            first_half_str = str(first_half_num)
            pal_str = make_palindrome(first_half_str)
            pal_num = int(pal_str)
            
            if pal_num % k == 0:
                return pal_str
        
        return ""
