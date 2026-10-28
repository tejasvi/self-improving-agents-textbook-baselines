from typing import List

class TrieNode:
    __slots__ = ('children', 'count', 'depth')
    def __init__(self, depth: int):
        self.children = {}
        self.count = 0
        self.depth = depth

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # If after removal we have fewer than k strings, answer is all zeros
        if n <= k:
            return [0] * n
        # Build trie and count occurrences of each prefix
        root = TrieNode(0)
        # keep reference to nodes for each word's path for later traversal
        paths = []  # list of list of TrieNode for each word
        for w in words:
            node = root
            cur_path = []
            for ch in w:
                if ch not in node.children:
                    node.children[ch] = TrieNode(node.depth + 1)
                node = node.children[ch]
                node.count += 1
                cur_path.append(node)
            paths.append(cur_path)
        # total_at_depth[d] = number of nodes at depth d with count >= k
        total_at_depth = {}
        max_depth_with_k = 0
        # Traverse all nodes via stack
        stack = [root]
        while stack:
            node = stack.pop()
            for child in node.children.values():
                stack.append(child)
            if node.depth == 0:
                continue
            if node.count >= k:
                total_at_depth[node.depth] = total_at_depth.get(node.depth, 0) + 1
                if node.depth > max_depth_with_k:
                    max_depth_with_k = node.depth
        # Compute answer for each word
        res = []
        for idx, w in enumerate(words):
            best = 0
            path = paths[idx]
            length = len(w)
            # If there exists a node deeper than this word with enough count, it is automatically valid
            if max_depth_with_k > length:
                best = max_depth_with_k
            # Scan the prefixes of the word
            for node in path:
                d = node.depth
                # case where this node itself could serve after removal
                if node.count >= k + 1:
                    best = max(best, d)
                # consider other nodes at same depth
                total = total_at_depth.get(d, 0)
                if total == 0:
                    continue
                if node.count >= k:
                    # this node is counted in total; need another one to stay valid
                    if total > 1:
                        best = max(best, d)
                else:
                    # this node not counted, any node with count>=k at this depth works
                    best = max(best, d)
            res.append(best)
        return res
