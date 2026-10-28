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
                cnt[nxt] += 1
                path.append(nxt)
                cur = nxt
            paths.append(path)

        # A: deepest node with count >= k+1 (usable regardless of removal)
        A = 0
        eq = []  # nodes with count == k
        for v in range(len(cnt)):
            if cnt[v] >= k + 1:
                if depth[v] > A:
                    A = depth[v]
            elif cnt[v] == k:
                eq.append(v)
        eq.sort(key=lambda v: -depth[v])

        ans = [0] * n
        if n - 1 < k:
            return ans
        for i in range(n):
            onpath = set(paths[i])
            best = A
            for v in eq:
                if v in onpath:
                    continue
                if depth[v] > best:
                    best = depth[v]
                break
            ans[i] = best
        return ans
