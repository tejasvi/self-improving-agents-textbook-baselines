from typing import *


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        children = [{}]
        cnt = [0]
        depth = [0]
        paths = []
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

        # nodes with count >= k, deepest first
        good = [v for v in range(1, len(children)) if cnt[v] >= k]
        good.sort(key=lambda v: -depth[v])

        res = [0] * n
        if n - 1 < k:
            return res
        for i in range(n):
            path = paths[i]
            best = 0
            # deepest ancestor still having count >= k after removal
            for v in path:
                if cnt[v] >= k + 1 and depth[v] > best:
                    best = depth[v]
            onpath = set(path)
            for v in good:
                if v not in onpath:
                    if depth[v] > best:
                        best = depth[v]
                    break
            res[i] = best
        return res
