import heapq
from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie; record depth and count of words through each node.
        children = [{}]
        depth = [0]
        cnt = [0]
        paths = []  # paths[i] = list of node ids for prefixes of words[i]
        for w in words:
            cur = 0
            cnt[0] += 1
            path = []
            for ch in w:
                nxt = children[cur].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[cur][ch] = nxt
                    children.append({})
                    depth.append(depth[cur] + 1)
                    cnt.append(0)
                cur = nxt
                cnt[cur] += 1
                path.append(cur)
            paths.append(path)

        maxd = max(depth)
        # cntDepth[d] = number of trie nodes at depth d with cnt >= k
        cntDepth = [0] * (maxd + 1)
        heap = []  # max-heap (negated) of depths, lazily cleaned
        for v in range(1, len(children)):
            if cnt[v] >= k:
                d = depth[v]
                if cntDepth[d] == 0:
                    heapq.heappush(heap, -d)
                cntDepth[d] += 1

        def inc(d):
            if cntDepth[d] == 0:
                heapq.heappush(heap, -d)
            cntDepth[d] += 1

        def dec(d):
            cntDepth[d] -= 1

        def query():
            while heap and cntDepth[-heap[0]] == 0:
                heapq.heappop(heap)
            return -heap[0] if heap else 0

        res = [0] * n
        for i in range(n):
            path = paths[i]
            # Deepest path node that stays >= k after removal.
            p = 0
            for v in path:
                if cnt[v] >= k + 1:
                    p = depth[v]
            # Temporarily remove path nodes that are currently in the set.
            for v in path:
                if cnt[v] >= k:
                    dec(depth[v])
            m = query()
            # Restore.
            for v in path:
                if cnt[v] >= k:
                    inc(depth[v])
            res[i] = max(p, m)
        return res
