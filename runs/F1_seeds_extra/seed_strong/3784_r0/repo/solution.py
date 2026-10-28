from typing import *


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n
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
        good = [v for v in range(1, len(depth)) if cnt[v] >= k]
        good.sort(key=lambda v: -depth[v])
        res = [0] * n
        for i in range(n):
            pset = set(paths[i])
            ans = 0
            for v in good:
                if v in pset and cnt[v] < k + 1:
                    continue
                ans = depth[v]
                break
            res[i] = ans
        return res
