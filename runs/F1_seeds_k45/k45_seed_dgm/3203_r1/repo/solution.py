from typing import List
from collections import Counter

class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        half = n // 2
        
        result = []
        
        for a, b, c, d in queries:
            # Check if we can make palindrome with rearrangements in [a,b] and [c,d]
            # First, check fixed positions (those not in rearrangeable ranges)
            
            # For each position i in [0, half), its mirror is n-1-i in [half, n)
            # If i is in [a, b], it can be rearranged
            # If n-1-i is in [c, d], it can be rearranged
            
            left_fixed_count = Counter()   # chars in fixed left positions
            right_fixed_count = Counter()  # chars in fixed right positions
            
            left_moveable_count = Counter()   # chars in moveable left positions
            right_moveable_count = Counter()  # chars in moveable right positions
            
            # Build counters for left side
            for i in range(half):
                if a <= i <= b:
                    left_moveable_count[s[i]] += 1
                else:
                    left_fixed_count[s[i]] += 1
            
            # Build counters for right side
            for i in range(half, n):
                if c <= i <= d:
                    right_moveable_count[s[i]] += 1
                else:
                    right_fixed_count[s[i]] += 1
            
            # Check if palindrome is possible
            valid = True
            
            # Check constraints for each mirror pair
            for i in range(half):
                mirror = n - 1 - i
                left_moveable = a <= i <= b
                right_moveable = c <= mirror <= d
                
                left_char = s[i]
                right_char = s[mirror]
                
                if not left_moveable and not right_moveable:
                    # Both positions are fixed - must match
                    if left_char != right_char:
                        valid = False
                        break
                elif left_moveable and not right_moveable:
                    # Left is moveable, right is fixed
                    # We need a char equal to right_char in left moveable range
                    if left_moveable_count[right_char] > 0:
                        left_moveable_count[right_char] -= 1
                    else:
                        valid = False
                        break
                elif not left_moveable and right_moveable:
                    # Right is moveable, left is fixed
                    # We need a char equal to left_char in right moveable range
                    if right_moveable_count[left_char] > 0:
                        right_moveable_count[left_char] -= 1
                    else:
                        valid = False
                        break
                else:
                    # Both are moveable - we'll handle this after checking fixed constraints
                    pass
            
            if not valid:
                result.append(False)
                continue
            
            # Now handle pairs where both are moveable
            # We need to match remaining characters from left and right moveable pools
            for i in range(half):
                mirror = n - 1 - i
                left_moveable = a <= i <= b
                right_moveable = c <= mirror <= d
                
                if left_moveable and right_moveable:
                    # Both are moveable, match greedily
                    left_char = s[i]
                    right_char = s[mirror]
                    
                    # Try to find matching characters
                    if left_moveable_count[right_char] > 0:
                        left_moveable_count[right_char] -= 1
                    elif right_moveable_count[left_char] > 0:
                        right_moveable_count[left_char] -= 1
                    else:
                        # Need to match from remaining pool
                        # This will be handled by checking if we can pair remaining chars
                        pass
            
            # Check if remaining characters can be paired
            # Remaining should have even counts for all characters
            remaining_left = left_moveable_count.copy()
            remaining_right = right_moveable_count.copy()
            
            # Try to match remaining
            for char in remaining_left:
                if remaining_left[char] > remaining_right[char]:
                    valid = False
                    break
            
            for char in remaining_right:
                if remaining_right[char] > remaining_left[char]:
                    valid = False
                    break
            
            result.append(valid)
        
        return result
