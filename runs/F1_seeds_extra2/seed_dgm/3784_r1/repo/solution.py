import heapq
from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # Build trie: children maps, counts of words passing through each node.
        children = [{}]
        cnt = [0]
        depth = [0]
        paths = []  # node ids along each word (excluding root)
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
                    cnt.append(0)
                    depth.append(depth[cur] + 1)
                cur = nxt
                cnt[cur] += 1
                path.append(cur)
            paths.append(path)

        maxd = max((len(w) for w in words), default=0)
        good = [0] * (maxd + 1)  # good[d]: number of nodes at depth d with cnt >= k
        for v in range(1, len(cnt)):
            if cnt[v] >= k:
                good[depth[v]] += 1
        heap = [-d for d in range(1, maxd + 1) if good[d] > 0]
        heapq.heapify(heap)

        res = [0] * n
        for i in range(n):
            if n - 1 >= k:
                path = paths[i]
                # remove word i
                for v in path:
                    if cnt[v] == k:
                        good[depth[v]] -= 1
                    cnt[v] -= 1
                # query deepest good depth
                while heap and good[-heap[0]] == 0:
                    heapq.heappop(heap)
                res[i] = -heap[0] if heap else 0
                # restore word i
                for v in path:
                    cnt[v] += 1
                    if cnt[v] == k:
                        d = depth[v]
                        good[d] += 1
                        if good[d] == 1:
                            heapq.heappush(heap, -d)
        return res
