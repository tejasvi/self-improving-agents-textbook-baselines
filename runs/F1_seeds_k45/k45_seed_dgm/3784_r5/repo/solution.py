from typing import List

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        
        # If we don't have enough strings after removal, return 0
        if n < k + 1:
            return [0] * n
        
        # Build a trie with prefix counts
        class TrieNode:
            def __init__(self):
                self.children = {}
                self.count = 0  # Number of words that pass through this node
        
        root = TrieNode()
        
        # Insert all words into the trie with their counts
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
                node.count += 1
        
        result = []
        
        # For each index i, find the longest common prefix among k strings
        # after removing the word at index i
        for i in range(n):
            # We need to find the longest prefix that appears in at least k strings
            # after removing word[i]
            
            removed_word = words[i]
            
            # Traverse the trie and find the longest prefix with count >= k
            # (after accounting for the removal of word[i])
            node = root
            prefix_length = 0
            
            for char in removed_word:
                if char not in node.children:
                    break
                node = node.children[char]
                # The count of this node minus 1 (for the removed word) should be >= k
                if node.count - 1 >= k:
                    prefix_length += 1
                else:
                    break
            
            result.append(prefix_length)
        
        return result
