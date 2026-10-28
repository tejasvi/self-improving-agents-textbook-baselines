from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        answer = [0] * n
        
        # For each index i, we need to find the longest common prefix
        # among any k strings from the remaining array
        for i in range(n):
            # Create array without element at index i
            remaining = words[:i] + words[i+1:]
            
            # If we don't have k strings left, answer is 0
            if len(remaining) < k:
                answer[i] = 0
                continue
            
            # Find the longest common prefix among k strings
            answer[i] = self.findLongestLCPAmongKStrings(remaining, k)
        
        return answer
    
    def findLongestLCPAmongKStrings(self, words: List[str], k: int) -> int:
        """
        Find the longest common prefix length among any k strings from words.
        """
        if not words or k > len(words):
            return 0
        
        max_length = min(len(word) for word in words)
        
        # Try each possible prefix length from max down to 0
        for prefix_len in range(max_length, -1, -1):
            # Group words by their prefix of length prefix_len
            prefix_count = {}
            for word in words:
                prefix = word[:prefix_len]
                prefix_count[prefix] = prefix_count.get(prefix, 0) + 1
            
            # Check if any prefix appears at least k times
            for count in prefix_count.values():
                if count >= k:
                    return prefix_len
        
        return 0
