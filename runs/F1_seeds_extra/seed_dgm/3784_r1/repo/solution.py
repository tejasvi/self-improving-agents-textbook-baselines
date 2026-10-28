import heapq
from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # Trie: children maps, depth and count of words passing through each node.
        children = [{}]
        depth = [0]
        cnt = [0]
        paths = []
        for w in words:
            cur = 0
            path = []
            for ch in w:
                nxt = children[cur].get(ch)
                if nxt is None:
                    nxt = len(depth)
                    children[cur][ch] = nxt
                    children.append({})
                    depth.append(depth[cur] + 1)
                    cnt.append(0)
                cur = nxt
                cnt[cur] += 1
                path.append(cur)
            paths.append(path)

        maxd = max((len(w) for w in words), default=0)
        good = [0] * (maxd + 1)  # good[d]: number of nodes at depth d with cnt >= k
        for v in range(1, len(depth)):
            if cnt[v] >= k:
                good[depth[v]] += 1
        heap = [-d for d in range(1, maxd + 1) if good[d] > 0]
        heapq.heapify(heap)

        def change(v, delta):
            old = cnt[v]
            new = old + delta
            cnt[v] = new
            was = old >= k
            now = new >= k
            if was != now:
                d = depth[v]
                if now:
                    good[d] += 1
                    if good[d] == 1:
                        heapq.heappush(heap, -d)
                else:
                    good[d] -= 1

        ans = [0] * n
        if n - 1 < k:
            return ans
        for i in range(n):
            path = paths[i]
            for v in path:
                change(v, -1)
            while heap and good[-heap[0]] == 0:
                heapq.heappop(heap)
            ans[i] = -heap[0] if heap else 0
            for v in path:
                change(v, +1)
        return ans
