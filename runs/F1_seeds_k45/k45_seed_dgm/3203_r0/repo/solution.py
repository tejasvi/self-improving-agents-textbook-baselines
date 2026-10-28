from typing import List
from collections import Counter

class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        results = []
        
        for a, b, c, d in queries:
            # Check if this query can make s a palindrome
            if self.canMakePalindrome(s, n, a, b, c, d):
                results.append(True)
            else:
                results.append(False)
        
        return results
    
    def canMakePalindrome(self, s: str, n: int, a: int, b: int, c: int, d: int) -> bool:
        """
        Check if we can make s a palindrome by rearranging s[a:b+1] and s[c:d+1]
        """
        # Collect characters from rearrangeable ranges
        left_chars = Counter(s[a:b+1])
        right_chars = Counter(s[c:d+1])
        
        # Check all mirror positions
        for i in range(n // 2):
            mirror = n - 1 - i
            left_char = s[i]
            right_char = s[mirror]
            
            # Case 1: Both positions are outside rearrangeable ranges
            if not (a <= i <= b) and not (c <= mirror <= d):
                if left_char != right_char:
                    return False
            
            # Case 2: Both positions are inside rearrangeable ranges
            elif (a <= i <= b) and (c <= mirror <= d):
                # We can arrange freely, but we need matching pairs
                # This will be checked later when we balance the characters
                pass
            
            # Case 3: Left position is in rearrangeable range, right is not
            elif (a <= i <= b) and not (c <= mirror <= d):
                # We need right_char in left range
                if left_chars[right_char] > 0:
                    left_chars[right_char] -= 1
                else:
                    return False
            
            # Case 4: Right position is in rearrangeable range, left is not
            elif not (a <= i <= b) and (c <= mirror <= d):
                # We need left_char in right range
                if right_chars[left_char] > 0:
                    right_chars[left_char] -= 1
                else:
                    return False
        
        # Now check if remaining characters in both ranges can be paired
        # Remaining chars in left_chars need to match with remaining in right_chars
        remaining_left = left_chars.copy()
        remaining_right = right_chars.copy()
        
        # Remove characters used in fixed positions
        for i in range(n // 2):
            mirror = n - 1 - i
            
            if (a <= i <= b) and (c <= mirror <= d):
                # Both are flexible - they must be paired from remaining chars
                pass
            elif (a <= i <= b) and not (c <= mirror <= d):
                # Already handled - right_char was removed from remaining_left
                pass
            elif not (a <= i <= b) and (c <= mirror <= d):
                # Already handled - left_char was removed from remaining_right
                pass
        
        # Check if remaining_left and remaining_right can form pairs
        # They must have the same character counts
        if remaining_left != remaining_right:
            return False
        
        return True
