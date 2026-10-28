class Solution:
    def largestPalindrome(self, n: int, k: int) -> str:
        # Special case: if n is 1
        if n == 1:
            for digit in range(9, 0, -1):
                if digit % k == 0:
                    return str(digit)
            return "0"
        
        # For n > 1, build palindrome from first half
        half_len = (n + 1) // 2
        
        def construct_palindrome(half_str):
            """Construct full palindrome from first half string"""
            if n % 2 == 0:
                # Even length: mirror the entire first half
                return half_str + half_str[::-1]
            else:
                # Odd length: mirror all but the middle digit
                return half_str + half_str[-2::-1]
        
        # Use BFS to build the first half
        # State: (position, current_half_string, remainder_mod_k)
        # We want to find the lexicographically largest first half where final palindrome is divisible by k
        
        from collections import deque
        
        # We'll use iterative deepening / greedy approach with backtracking
        # For each position from left to right, try digits 9 down to 0/1
        # But we need to track what remainder the palindrome will have
        
        def get_remainder(half_str):
            """Calculate what remainder the palindrome will have when divided by k"""
            palindrome_str = construct_palindrome(half_str)
            palindrome_num = int(palindrome_str) % k
            return palindrome_num
        
        # Greedy search with early termination
        # Start with 9s and work our way down
        max_half = 10 ** half_len - 1
        min_half = 10 ** (half_len - 1)
        
        for half_val in range(max_half, min_half - 1, -1):
            half_str = str(half_val)
            if get_remainder(half_str) == 0:
                return construct_palindrome(half_str)
        
        return ""
