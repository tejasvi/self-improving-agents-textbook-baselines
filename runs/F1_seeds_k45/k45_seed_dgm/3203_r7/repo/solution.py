from typing import List
from collections import Counter

class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        n = len(s)
        half = n // 2
        answer = []
        
        for a, b, c, d in queries:
            if self._canMakePalindrome(s, a, b, c, d, half, n):
                answer.append(True)
            else:
                answer.append(False)
        
        return answer
    
    def _canMakePalindrome(self, s: str, a: int, b: int, c: int, d: int, half: int, n: int) -> bool:
        """
        More careful check for palindrome possibility
        """
        left_needed = Counter()  # What left side needs to provide
        right_needed = Counter()  # What right side needs to provide
        
        for i in range(half):
            mirror_i = n - 1 - i
            
            left_rearrangeable = a <= i <= b
            right_rearrangeable = c <= mirror_i <= d
            
            if not left_rearrangeable and not right_rearrangeable:
                # Both fixed - must match
                if s[i] != s[mirror_i]:
                    return False
            elif left_rearrangeable and not right_rearrangeable:
                # Left can change, right is fixed
                left_needed[s[mirror_i]] += 1
            elif not left_rearrangeable and right_rearrangeable:
                # Left is fixed, right can change
                right_needed[s[i]] += 1
            # If both rearrangeable, we'll handle later
        
        # Get available characters
        left_available = Counter(s[a:b+1])
        right_available = Counter(s[c:d+1])
        
        # Check if we can satisfy fixed requirements
        for char, count in left_needed.items():
            if left_available[char] < count:
                return False
            left_available[char] -= count
        
        for char, count in right_needed.items():
            if right_available[char] < count:
                return False
            right_available[char] -= count
        
        # Now for positions where both are rearrangeable, we have leftover characters
        # We need to check if we can form a palindrome from the leftover characters
        # combined with the positions that are both rearrangeable
        
        # Collect all positions that are both rearrangeable
        both_left_indices = []
        both_right_indices = []
        
        for i in range(half):
            mirror_i = n - 1 - i
            if a <= i <= b and c <= mirror_i <= d:
                both_left_indices.append(i)
                both_right_indices.append(mirror_i)
        
        # For these positions, we have a shared pool of characters from both sides
        shared_pool = left_available + right_available
        
        # Check if shared pool can form a palindrome for these pairs
        # Each pair (i, mirror_i) needs matching characters
        num_pairs = len(both_left_indices)
        
        if num_pairs == 0:
            # No shared pairs, everything is already checked
            return True
        
        # Count total characters needed (should equal shared_pool size for num_pairs positions)
        # We need num_pairs matching pairs from shared_pool
        total_needed = 2 * num_pairs
        total_available = sum(shared_pool.values())
        
        if total_available != total_needed:
            return False
        
        # Check if we can form num_pairs matching pairs
        # This means we need an even count for each character (no odd counts)
        for count in shared_pool.values():
            if count % 2 != 0:
                return False
        
        return True
