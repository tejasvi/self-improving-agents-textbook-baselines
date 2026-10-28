from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        result = []
        
        # For each removal index
        for remove_idx in range(n):
            # If remaining array has fewer than k strings, answer is 0
            if n - 1 < k:
                result.append(0)
                continue
            
            # Get remaining words (all except remove_idx)
            remaining = [words[i] for i in range(n) if i != remove_idx]
            
            # Find the longest common prefix among any k strings from remaining
            max_prefix_len = self._find_longest_prefix_for_k_strings(remaining, k)
            result.append(max_prefix_len)
        
        return result
    
    def _find_longest_prefix_for_k_strings(self, words: List[str], k: int) -> int:
        """Find the longest common prefix among any k strings from the given list."""
        if len(words) < k:
            return 0
        
        # Get the minimum length to avoid index out of bounds
        min_len = min(len(word) for word in words)
        
        # Binary search on the length of the prefix
        left, right = 0, min_len
        result = 0
        
        while left <= right:
            mid = (left + right) // 2
            
            # Check if there exists a prefix of length mid that appears in at least k strings
            if self._can_find_k_strings_with_prefix_len(words, k, mid):
                result = mid
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    def _can_find_k_strings_with_prefix_len(self, words: List[str], k: int, prefix_len: int) -> int:
        """Check if there exists a prefix of given length that appears in at least k strings."""
        # Group words by their prefix of length prefix_len
        prefix_count = {}
        
        for word in words:
            prefix = word[:prefix_len]
            prefix_count[prefix] = prefix_count.get(prefix, 0) + 1
        
        # Check if any prefix appears in at least k strings
        for count in prefix_count.values():
            if count >= k:
                return True
        
        return False
