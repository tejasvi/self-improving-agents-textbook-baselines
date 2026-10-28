from typing import List
from collections import Counter

class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        half = n // 2
        results = []
        
        for a, b, c, d in queries:
            # Check if we can make a palindrome with the given rearrangeable ranges
            if self.canMakePalindrome(s, a, b, c, d, half):
                results.append(True)
            else:
                results.append(False)
        
        return results
    
    def canMakePalindrome(self, s: str, a: int, b: int, c: int, d: int, half: int) -> bool:
        n = len(s)
        
        # Collect characters in rearrangeable regions
        left_chars = Counter(s[a:b+1])
        right_chars = Counter(s[c:d+1])
        
        # Process each palindrome pair
        for i in range(half):
            mirror = n - 1 - i
            
            char_i = s[i]
            char_mirror = s[mirror]
            
            # Check if positions are in rearrangeable ranges
            i_in_left = a <= i <= b
            mirror_in_right = c <= mirror <= d
            
            if not i_in_left and not mirror_in_right:
                # Neither can be rearranged - they must already match
                if char_i != char_mirror:
                    return False
            elif i_in_left and not mirror_in_right:
                # Only left position can be rearranged
                # Position mirror is fixed as char_mirror
                # Position i needs to have char_mirror
                if left_chars[char_mirror] > 0:
                    left_chars[char_mirror] -= 1
                else:
                    return False
            elif not i_in_left and mirror_in_right:
                # Only right position can be rearranged
                # Position i is fixed as char_i
                # Position mirror needs to have char_i
                if right_chars[char_i] > 0:
                    right_chars[char_i] -= 1
                else:
                    return False
            else:  # both i_in_left and mirror_in_right
                # Both positions can be rearranged
                # We need to match them - prefer using matching characters if available
                # Try to find char_mirror in left and char_i in right
                if left_chars[char_mirror] > 0 and right_chars[char_i] > 0:
                    left_chars[char_mirror] -= 1
                    right_chars[char_i] -= 1
                # Try swapped matching
                elif left_chars[char_i] > 0 and right_chars[char_mirror] > 0:
                    left_chars[char_i] -= 1
                    right_chars[char_mirror] -= 1
                else:
                    return False
        
        return True
