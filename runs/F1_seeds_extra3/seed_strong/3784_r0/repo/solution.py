from typing import *


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie: children, count of words through node, depth.
        children = [{}]
        cnt = [0]
        depth = [0]
        paths = []  # per word: list of node ids along its path (depth 1..L)
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

        # Good nodes (count >= k), sorted by depth descending.
        good = [v for v in range(1, len(children)) if cnt[v] >= k]
        good.sort(key=lambda v: -depth[v])

        res = [0] * n
        for i in range(n):
            path = paths[i]
            pset = set(path)
            # (a) deepest good node not on path (its count is unchanged)
            best = 0
            for v in good:
                if v not in pset:
                    best = depth[v]
                    break
            # (b) deepest path node whose count stays >= k after removal
            for v in reversed(path):
                if cnt[v] - 1 >= k:
                    if depth[v] > best:
                        best = depth[v]
                    break
            res[i] = best
        return res
