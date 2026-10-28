from typing import List
from collections import defaultdict
from itertools import combinations

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        result = []
        
        def get_lcp(string_list):
            """Get the longest common prefix of a list of strings."""
            if not string_list:
                return 0
            
            min_len = min(len(s) for s in string_list)
            lcp_len = 0
            
            for char_idx in range(min_len):
                char = string_list[0][char_idx]
                if all(s[char_idx] == char for s in string_list):
                    lcp_len += 1
                else:
                    break
            
            return lcp_len
        
        # For each removal index
        for i in range(n):
            # Create remaining array without element at index i
            remaining = words[:i] + words[i+1:]
            
            # If fewer than k strings remain, answer is 0
            if len(remaining) < k:
                result.append(0)
                continue
            
            max_lcp = 0
            
            # Try all combinations of k strings
            for combo in combinations(range(len(remaining)), k):
                selected = [remaining[j] for j in combo]
                lcp_len = get_lcp(selected)
                max_lcp = max(max_lcp, lcp_len)
            
            result.append(max_lcp)
        
        return result
