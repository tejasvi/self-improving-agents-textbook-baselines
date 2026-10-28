from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        best_len = 0
        best_nodes = 1
        # last depth at which each value occurs on the current root-to-node path
        pw = [0] * n
        last = {}
        # pref[d] = distance from root to the node at depth d on current path
        pref = []
        # left = smallest depth index that can start a special path ending at current node
        left = 0

        # iterative DFS; entries: (node, parent, depth, enter_flag, saved_left, saved_last)
        stack = [(0, -1, 0, True)]
        saved = {}  # node -> (old_left, old_last_depth)
        while stack:
            node, parent, depth, enter = stack.pop()
            if enter:
                val = nums[node]
                prev_depth = last.get(val, -1)
                saved[node] = (left, prev_depth)
                if prev_depth + 1 > left:
                    left = prev_depth + 1
                last[val] = depth
                # set prefix distance for this depth
                if depth == 0:
                    pref.append(0)
                else:
                    pref.append(pref[depth - 1] + pw[node])
                # evaluate paths ending at node
                length = pref[depth] - pref[left]
                nodes = depth - left + 1
                if length > best_len or (length == best_len and nodes < best_nodes):
                    best_len = length
                    best_nodes = nodes
                stack.append((node, parent, depth, False))
                for child, w in adj[node]:
                    if child != parent:
                        pw[child] = w
                        stack.append((child, node, depth + 1, True))
            else:
                old_left, prev_depth = saved.pop(node)
                val = nums[node]
                if prev_depth == -1:
                    del last[val]
                else:
                    last[val] = prev_depth
                left = old_left
                pref.pop()
        return [best_len, best_nodes]
