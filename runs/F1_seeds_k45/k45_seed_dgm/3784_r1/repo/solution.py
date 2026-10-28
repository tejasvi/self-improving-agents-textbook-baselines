from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n < k:
            return [0] * n
        
        result = [0] * n
        
        # For each removal index
        for remove_idx in range(n):
            # Get the remaining words
            remaining = words[:remove_idx] + words[remove_idx + 1:]
            
            if len(remaining) < k:
                result[remove_idx] = 0
                continue
            
            # Find the longest common prefix among any k strings in remaining
            max_lcp_len = self._find_max_lcp(remaining, k)
            result[remove_idx] = max_lcp_len
        
        return result
    
    def _find_max_lcp(self, words: List[str], k: int) -> int:
        """Find the length of the longest common prefix among any k words"""
        if len(words) < k:
            return 0
        
        # Build a trie and track counts at each node
        trie = {}
        
        for word in words:
            node = trie
            for char in word:
                if char not in node:
                    node[char] = {'count': 0}
                node[char]['count'] += 1
                node = node[char]
        
        # Find the deepest level where we have at least k words
        def dfs(node, depth):
            max_depth = 0
            
            # Check if we have k or more words at this node
            for char in node:
                if node[char]['count'] >= k:
                    # Continue going deeper
                    child_depth = dfs(node[char], depth + 1)
                    max_depth = max(max_depth, child_depth)
            
            # If this node has k or more words, this is a valid depth
            if max_depth == 0:  # Leaf node or no children with k+ words
                # Check the current level
                for char in node:
                    if node[char]['count'] >= k:
                        max_depth = depth + 1
            
            return max_depth
        
        # Actually, let's use a simpler approach
        max_len = 0
        
        def traverse(node, depth):
            nonlocal max_len
            
            # Check if current path can have k words
            for char in node:
                if node[char]['count'] >= k:
                    max_len = max(max_len, depth + 1)
                    traverse(node[char], depth + 1)
        
        traverse(trie, 0)
        return max_len
