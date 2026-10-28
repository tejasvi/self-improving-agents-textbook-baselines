from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        """
        For each index i, remove the i-th element and find the longest common prefix
        among any k strings from the remaining array.
        """
        n = len(words)
        result = []
        
        for i in range(n):
            # Create remaining array without index i
            remaining = words[:i] + words[i+1:]
            
            # If remaining array has fewer than k strings, answer is 0
            if len(remaining) < k:
                result.append(0)
                continue
            
            # Find the longest common prefix among any k strings
            lcp_length = self._findLongestCommonPrefixLength(remaining, k)
            result.append(lcp_length)
        
        return result
    
    def _findLongestCommonPrefixLength(self, words: List[str], k: int) -> int:
        """
        Find the longest common prefix length among any k strings.
        Uses a trie-based approach where we track how many strings have each prefix.
        """
        if not words or k > len(words):
            return 0
        
        # Build a trie and track counts
        class TrieNode:
            def __init__(self):
                self.children = {}
                self.count = 0  # Number of strings passing through this node
        
        root = TrieNode()
        
        # Insert all words into trie
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                node.count += 1
        
        # Find the deepest node where count >= k
        max_lcp = 0
        
        def dfs(node, depth):
            nonlocal max_lcp
            if node.count >= k:
                max_lcp = max(max_lcp, depth)
            for child in node.children.values():
                dfs(child, depth + 1)
        
        for child in root.children.values():
            dfs(child, 1)
        
        return max_lcp
