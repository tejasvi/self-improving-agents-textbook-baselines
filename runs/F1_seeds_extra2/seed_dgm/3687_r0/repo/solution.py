from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        last = {}                 # value -> depth of its latest occurrence on path
        path_dist = [0] * (n + 1)  # distance from root to node at each depth on path
        best_len = 0
        best_nodes = 1

        # Stack entries: (node, parent, depth, dist, saved_left, saved_prev, phase)
        # phase 0 = enter, phase 1 = exit
        left_holder = [0]         # current left boundary (min valid depth)
        stack = [(0, -1, 0, 0, 0, None, 0)]
        saved = {}
        while stack:
            v, p, d, dist, _, _, phase = stack.pop()
            if phase == 1:
                # exit: restore state
                prev_left, val, prev_occ = saved.pop(v)
                left_holder[0] = prev_left
                if prev_occ is None:
                    del last[val]
                else:
                    last[val] = prev_occ
                continue

            val = nums[v]
            prev_occ = last.get(val)
            saved[v] = (left_holder[0], val, prev_occ)
            if prev_occ is not None and prev_occ + 1 > left_holder[0]:
                left_holder[0] = prev_occ + 1
            left = left_holder[0]
            last[val] = d
            path_dist[d] = dist

            length = dist - path_dist[left]
            nodes = d - left + 1
            if length > best_len or (length == best_len and nodes < best_nodes):
                best_len = length
                best_nodes = nodes

            stack.append((v, p, d, dist, 0, None, 1))
            for u, w in adj[v]:
                if u != p:
                    stack.append((u, v, d + 1, dist + w, 0, None, 0))

        return [best_len, best_nodes]
