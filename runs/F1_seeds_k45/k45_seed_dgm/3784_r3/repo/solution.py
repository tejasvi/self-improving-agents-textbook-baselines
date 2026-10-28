from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        """
        Find the length of the longest common prefix among any k strings 
        after removing the i-th element.
        
        Args:
            words: List of strings
            k: Number of strings to select
            
        Returns:
            List of integers where answer[i] is the longest common prefix length
            after removing the i-th element
        """
        n = len(words)
        result = []
        
        # For each index i, remove the i-th element and find the answer
        for remove_idx in range(n):
            # Create remaining array
            remaining = words[:remove_idx] + words[remove_idx + 1:]
            
            # If remaining has fewer than k strings, answer is 0
            if len(remaining) < k:
                result.append(0)
                continue
            
            # Find the longest common prefix among any k strings
            max_prefix_len = self._findLongestCommonPrefixForK(remaining, k)
            result.append(max_prefix_len)
        
        return result
    
    def _findLongestCommonPrefixForK(self, words: List[str], k: int) -> int:
        """
        Find the longest common prefix among any k strings in the given list.
        
        Args:
            words: List of strings to search
            k: Number of strings to select
            
        Returns:
            Length of the longest common prefix
        """
        # Find the minimum length among all words
        if not words:
            return 0
        
        min_len = min(len(word) for word in words)
        
        # Try each possible prefix length from the maximum down to 1
        for prefix_len in range(min_len, 0, -1):
            # Check if we can find k strings with the same prefix of this length
            prefix_count = {}
            
            for word in words:
                prefix = word[:prefix_len]
                prefix_count[prefix] = prefix_count.get(prefix, 0) + 1
                
                # If we found a prefix that appears k times, we're done
                if prefix_count[prefix] >= k:
                    return prefix_len
            
        return 0
