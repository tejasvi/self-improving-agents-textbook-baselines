from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        last = {}                  # value -> depth of its latest occurrence on current root path
        path_dist = [0] * (n + 1)  # path_dist[d] = distance from root to ancestor at depth d
        best_len, best_nodes = 0, 1

        # Stack entries: (node, parent, depth, dist, left, old_last, is_enter)
        # left = smallest depth allowed for the top of a unique-valued path ending at node
        stack = [(0, -1, 0, 0, 0, -1, True)]
        while stack:
            node, parent, depth, dist, left, old, enter = stack.pop()
            x = nums[node]
            if enter:
                prev = last.get(x, -1)
                new_left = max(left, prev + 1)
                path_dist[depth] = dist
                length = dist - path_dist[new_left]
                nodes = depth - new_left + 1
                if length > best_len or (length == best_len and nodes < best_nodes):
                    best_len, best_nodes = length, nodes
                stack.append((node, parent, depth, dist, left, prev, False))
                last[x] = depth
                for child, w in adj[node]:
                    if child != parent:
                        stack.append((child, node, depth + 1, dist + w, new_left, -1, True))
            else:
                if old == -1:
                    del last[x]
                else:
                    last[x] = old
        return [best_len, best_nodes]
