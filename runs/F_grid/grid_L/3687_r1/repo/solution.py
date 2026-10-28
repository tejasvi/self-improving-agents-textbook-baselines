from typing import List


class Solution:
    def longestSpecialPath(self, edges: List[List[int]], nums: List[int]) -> List[int]:
        n = len(nums)
        adj = [[] for _ in range(n)]
        for u, v, w in edges:
            adj[u].append((v, w))
            adj[v].append((u, w))

        last = {}              # value -> depth of its latest occurrence on the current root path
        pref = [0] * (n + 1)   # pref[d] = root distance of the node at depth d on the current path
        best_len, best_cnt = 0, 1
        left = 0               # smallest depth of an ancestor allowed as the path's top node

        visited = [False] * n
        visited[0] = True
        # Stack entries: (node, depth, dist, phase, saved_prev, saved_left)
        stack = [(0, 0, 0, 0, None, None)]
        while stack:
            node, d, dist, phase, saved_prev, saved_left = stack.pop()
            val = nums[node]
            if phase == 0:
                prev = last.get(val, -1)
                pref[d] = dist
                stack.append((node, d, dist, 1, prev, left))
                if prev + 1 > left:
                    left = prev + 1
                last[val] = d
                length = dist - pref[left]
                cnt = d - left + 1
                if length > best_len or (length == best_len and cnt < best_cnt):
                    best_len, best_cnt = length, cnt
                for child, w in adj[node]:
                    if not visited[child]:
                        visited[child] = True
                        stack.append((child, d + 1, dist + w, 0, None, None))
            else:
                if saved_prev == -1:
                    del last[val]
                else:
                    last[val] = saved_prev
                left = saved_left

        return [best_len, best_cnt]
