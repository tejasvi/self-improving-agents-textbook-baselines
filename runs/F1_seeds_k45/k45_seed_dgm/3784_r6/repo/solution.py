from typing import List
from collections import defaultdict

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        result = []
        
        # For each index i to remove
        for i in range(n):
            # Build remaining array without index i
            remaining = words[:i] + words[i+1:]
            
            # If remaining has fewer than k elements, answer is 0
            if len(remaining) < k:
                result.append(0)
                continue
            
            # Find the longest common prefix among any k strings
            max_prefix_length = 0
            
            # Try each possible prefix length
            max_word_length = max(len(word) for word in remaining)
            
            for prefix_len in range(1, max_word_length + 1):
                # Count how many strings have each prefix of this length
                prefix_count = defaultdict(int)
                
                for word in remaining:
                    if len(word) >= prefix_len:
                        prefix = word[:prefix_len]
                        prefix_count[prefix] += 1
                
                # Check if any prefix appears in at least k strings
                for prefix, count in prefix_count.items():
                    if count >= k:
                        max_prefix_length = prefix_len
                        break
            
            result.append(max_prefix_length)
        
        return result
