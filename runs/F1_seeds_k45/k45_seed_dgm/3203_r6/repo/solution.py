from typing import List
from collections import Counter

class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        half = n // 2
        result = []
        
        for a, b, c, d in queries:
            # Check if we can make palindrome with this query
            if self.canMakePalindrome(s, a, b, c, d, half):
                result.append(True)
            else:
                result.append(False)
        
        return result
    
    def canMakePalindrome(self, s: str, a: int, b: int, c: int, d: int, half: int) -> bool:
        n = len(s)
        
        # Collect characters that can be rearranged
        # Left side rearrangeable: [a, b]
        # Right side rearrangeable: [c, d]
        left_available = Counter(s[a:b+1])
        right_available = Counter(s[c:d+1])
        
        # For palindrome checking, pair up positions
        # Position i should match with position n-1-i
        
        # We need to check each pair (i, n-1-i)
        for i in range(half):
            mirror = n - 1 - i
            
            left_pos_in_range = a <= i <= b  # position i is in left rearrangeable range
            right_pos_in_range = c <= mirror <= d  # position mirror is in right rearrangeable range
            
            char_i = s[i]
            char_mirror = s[mirror]
            
            # Case 1: Both positions are fixed (not rearrangeable)
            if not left_pos_in_range and not right_pos_in_range:
                if char_i != char_mirror:
                    return False
            
            # Case 2: Position i is rearrangeable, mirror is fixed
            elif left_pos_in_range and not right_pos_in_range:
                # We need to have char_mirror available in left_available
                if left_available[char_mirror] > 0:
                    left_available[char_mirror] -= 1
                else:
                    return False
            
            # Case 3: Position i is fixed, mirror is rearrangeable
            elif not left_pos_in_range and right_pos_in_range:
                # We need to have char_i available in right_available
                if right_available[char_i] > 0:
                    right_available[char_i] -= 1
                else:
                    return False
            
            # Case 4: Both positions are rearrangeable
            else:
                # We have freedom here, but we need to track what we're using
                # For now, prefer using from left_available if possible
                if left_available[char_mirror] > 0:
                    left_available[char_mirror] -= 1
                elif right_available[char_mirror] > 0:
                    right_available[char_mirror] -= 1
                else:
                    return False
        
        return True
