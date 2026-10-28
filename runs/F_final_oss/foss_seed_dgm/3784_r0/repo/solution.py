from typing import List

class TrieNode:
    __slots__ = ("children", "count", "depth")
    def __init__(self, depth: int):
        self.children = {}
        self.count = 0
        self.depth = depth

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # If after removal there are fewer than k strings, answer is 0 for all positions
        if n - 1 < k:
            return [0] * n
        # Build trie and store node path for each word (excluding root)
        root = TrieNode(0)
        word_nodes: List[List[TrieNode]] = []
        for w in words:
            node = root
            path = []
            for ch in w:
                if ch not in node.children:
                    node.children[ch] = TrieNode(node.depth + 1)
                node = node.children[ch]
                node.count += 1
                path.append(node)
            word_nodes.append(path)
        # Gather nodes by depth
        from collections import defaultdict
        depth_nodes = defaultdict(list)  # depth -> list of nodes at that depth
        stack = [root]
        while stack:
            node = stack.pop()
            if node is not root:
                depth_nodes[node.depth].append(node)
            for child in node.children.values():
                stack.append(child)
        # For each depth compute max1, count of max1, and max2
        depth_info = {}  # depth -> (max1, cnt_max1, max2)
        valid_depths = []  # depths where some prefix appears at least k times
        for d, nodes in depth_nodes.items():
            max1 = -1
            max2 = -1
            cnt_max1 = 0
            for nd in nodes:
                c = nd.count
                if c > max1:
                    max2 = max1
                    max1 = c
                    cnt_max1 = 1
                elif c == max1:
                    cnt_max1 += 1
                elif c > max2:
                    max2 = c
            if max1 >= k:
                valid_depths.append(d)
            depth_info[d] = (max1, cnt_max1, max2)
        # Sort depths increasingly for binary search (monotonic property)
        valid_depths.sort()
        ans = [0] * n
        # Helper to compute effective maximum count at depth d after removing word i
        def effective_count(i: int, d: int) -> int:
            max1, cnt_max1, max2 = depth_info[d]
            path = word_nodes[i]
            if d <= len(path):
                node = path[d - 1]
                if node.count == max1 and cnt_max1 == 1:
                    # this word is the unique contributor to the maximal count
                    return max2
            return max1
        # For each word, binary search the greatest depth with effective >= k
        for i in range(n):
            lo, hi = 0, len(valid_depths) - 1
            best = 0
            while lo <= hi:
                mid = (lo + hi) // 2
                d = valid_depths[mid]
                if effective_count(i, d) >= k:
                    best = d
                    lo = mid + 1
                else:
                    hi = mid - 1
            ans[i] = best
        return ans
