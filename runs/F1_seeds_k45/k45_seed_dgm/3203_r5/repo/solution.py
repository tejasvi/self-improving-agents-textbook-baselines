from typing import List
from collections import Counter

class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        half = n // 2
        result = []
        
        for a, b, c, d in queries:
            # Check if we can make a palindrome with the given rearrangeable ranges
            if self.canMakePalindrome(s, a, b, c, d, half):
                result.append(True)
            else:
                result.append(False)
        
        return result
    
    def canMakePalindrome(self, s: str, a: int, b: int, c: int, d: int, half: int) -> bool:
        n = len(s)
        
        # Collect characters from rearrangeable ranges
        left_chars = []
        right_chars = []
        
        for i in range(a, b + 1):
            left_chars.append(s[i])
        
        for i in range(c, d + 1):
            right_chars.append(s[i])
        
        left_counter = Counter(left_chars)
        right_counter = Counter(right_chars)
        
        # For each position pair (i, n-1-i) where i < half
        for i in range(half):
            mirror = n - 1 - i
            
            is_i_in_range = a <= i <= b
            is_mirror_in_range = c <= mirror <= d
            
            if not is_i_in_range and not is_mirror_in_range:
                # Both positions are fixed, must match for palindrome
                if s[i] != s[mirror]:
                    return False
            elif is_i_in_range and not is_mirror_in_range:
                # Position i is rearrangeable, mirror is fixed
                # We need character s[mirror] in left_pool
                if left_counter[s[mirror]] > 0:
                    left_counter[s[mirror]] -= 1
                else:
                    return False
            elif not is_i_in_range and is_mirror_in_range:
                # Position mirror is rearrangeable, i is fixed
                # We need character s[i] in right_pool
                if right_counter[s[i]] > 0:
                    right_counter[s[i]] -= 1
                else:
                    return False
            else:
                # Both positions are rearrangeable
                # We need matching pair from the combined pools
                # Try to match them
                
                # Check if we can find a matching pair
                found = False
                
                # Try using a character from left pool
                for char in left_counter:
                    if left_counter[char] > 0 and right_counter[char] > 0:
                        left_counter[char] -= 1
                        right_counter[char] -= 1
                        found = True
                        break
                
                if not found:
                    return False
        
        return True
