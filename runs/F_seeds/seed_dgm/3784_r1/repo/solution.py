import heapq
from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie; node 0 is root. Store children, count, depth.
        children = [{}]
        cnt = [0]
        depth = [0]
        paths = []  # node indices along each word's path (excluding root)
        for w in words:
            cur = 0
            path = []
            for ch in w:
                nxt = children[cur].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[cur][ch] = nxt
                    children.append({})
                    cnt.append(0)
                    depth.append(depth[cur] + 1)
                cur = nxt
                cnt[cur] += 1
                path.append(cur)
            paths.append(path)

        # good[d] = number of nodes at depth d with cnt >= k
        good = {}
        heap = []  # lazy max-heap of negative depths with good[d] > 0
        for node in range(1, len(cnt)):
            if cnt[node] >= k:
                d = depth[node]
                good[d] = good.get(d, 0) + 1
        for d in good:
            heap.append(-d)
        heapq.heapify(heap)

        def query():
            while heap and good.get(-heap[0], 0) == 0:
                heapq.heappop(heap)
            return -heap[0] if heap else 0

        ans = [0] * n
        for i in range(n):
            # Remove word i.
            for node in paths[i]:
                old = cnt[node]
                cnt[node] = old - 1
                if old >= k and old - 1 < k:
                    good[depth[node]] -= 1
            if n - 1 >= k:
                ans[i] = query()
            # Restore word i.
            for node in paths[i]:
                old = cnt[node]
                cnt[node] = old + 1
                if old < k and old + 1 >= k:
                    d = depth[node]
                    prev = good.get(d, 0)
                    good[d] = prev + 1
                    if prev == 0:
                        heapq.heappush(heap, -d)
        return ans
