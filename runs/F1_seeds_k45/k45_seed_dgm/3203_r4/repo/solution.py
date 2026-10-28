from typing import List
from collections import Counter

class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        """
        For each query, determine if we can rearrange the specified substrings
        to make the entire string a palindrome.
        """
        n = len(s)
        results = []
        
        for a, b, c, d in queries:
            if self._canMakePalindrome(s, n, a, b, c, d):
                results.append(True)
            else:
                results.append(False)
        
        return results
    
    def _canMakePalindrome(self, s: str, n: int, a: int, b: int, c: int, d: int) -> bool:
        """
        Check if we can make the string a palindrome with the given rearrangeable regions.
        """
        # Collect all characters we can use from rearrangeable regions
        left_chars = Counter(s[a:b+1])
        right_chars = Counter(s[c:d+1])
        
        # Check each palindrome pair (i, mirror)
        for i in range(n // 2):
            mirror = n - 1 - i
            
            i_in_left = (a <= i <= b)
            mirror_in_right = (c <= mirror <= d)
            
            # Case 1: Both positions are fixed (not rearrangeable)
            if not i_in_left and not mirror_in_right:
                if s[i] != s[mirror]:
                    return False
            
            # Case 2: Only position i is rearrangeable (left side)
            elif i_in_left and not mirror_in_right:
                # Position i can be any character from left_chars
                # Position mirror is fixed to s[mirror]
                # So we need s[mirror] to be available in left_chars
                char_needed = s[mirror]
                if left_chars[char_needed] > 0:
                    left_chars[char_needed] -= 1
                else:
                    return False
            
            # Case 3: Only position mirror is rearrangeable (right side)
            elif not i_in_left and mirror_in_right:
                # Position mirror can be any character from right_chars
                # Position i is fixed to s[i]
                # So we need s[i] to be available in right_chars
                char_needed = s[i]
                if right_chars[char_needed] > 0:
                    right_chars[char_needed] -= 1
                else:
                    return False
            
            # Case 4: Both positions are rearrangeable
            # We'll handle this after processing all fixed/one-sided cases
        
        # After assigning characters for fixed positions,
        # the remaining characters must be able to pair up
        # For positions where both i and mirror are rearrangeable,
        # we need to place characters at both positions that are the same.
        
        # Merge remaining characters - they need to pair up for palindrome
        total_remaining = Counter()
        for char, count in left_chars.items():
            total_remaining[char] += count
        for char, count in right_chars.items():
            total_remaining[char] += count
        
        # For a valid palindrome, all remaining characters must come in pairs
        # (since each pair at positions i and mirror must have the same character)
        for char, count in total_remaining.items():
            if count % 2 != 0:
                return False
        
        return True
