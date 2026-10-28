from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        best_len, best_cnt = 0, 1
        last = {}                    # value -> depth of its nearest ancestor on current path
        pd = [0] * (n + 1)           # pd[depth] = distance from root to node at that depth
        L = 0                        # left boundary (depth) of the window of unique values
        # stack entries: (node, parent, depth, dist, is_exit, saved_prev, saved_L)
        stack = [(0, -1, 0, 0, False, None, None)]
        while stack:
            node, parent, d, dist, is_exit, prev, oldL = stack.pop()
            v = nums[node]
            if is_exit:
                if prev == -1:
                    del last[v]
                else:
                    last[v] = prev
                L = oldL
                continue
            prev = last.get(v, -1)
            oldL = L
            if prev + 1 > L:
                L = prev + 1
            last[v] = d
            pd[d] = dist
            length = dist - pd[L]
            cnt = d - L + 1
            if length > best_len or (length == best_len and cnt < best_cnt):
                best_len, best_cnt = length, cnt
            stack.append((node, parent, d, dist, True, prev, oldL))
            for nxt, w in adj[node]:
                if nxt != parent:
                    stack.append((nxt, node, d + 1, dist + w, False, None, None))
        return [best_len, best_cnt]
