from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        # Per-depth state along the current root-to-node path.
        dist_at = [0] * (n + 1)   # root distance of the node at depth d
        left_at = [0] * (n + 1)   # first depth of the unique-value window ending at depth d
        last = {}                 # value -> deepest depth on current path holding it
        best_len, best_cnt = 0, 1

        # Stack entries: (node, parent, depth, root_distance, saved_prev, phase)
        stack = [(0, -1, 0, 0, None, 0)]
        while stack:
            node, parent, d, dist, saved, phase = stack.pop()
            x = nums[node]
            if phase == 0:
                prev = last.get(x, -1)
                last[x] = d
                dist_at[d] = dist
                left_at[d] = max(left_at[d - 1], prev + 1) if d > 0 else 0
                length = dist - dist_at[left_at[d]]
                cnt = d - left_at[d] + 1
                if length > best_len or (length == best_len and cnt < best_cnt):
                    best_len, best_cnt = length, cnt
                stack.append((node, parent, d, dist, prev, 1))
                for child, w in adj[node]:
                    if child != parent:
                        stack.append((child, node, d + 1, dist + w, None, 0))
            else:
                # Exiting node: restore the previous deepest occurrence of x.
                if saved == -1:
                    del last[x]
                else:
                    last[x] = saved

        return [best_len, best_cnt]
