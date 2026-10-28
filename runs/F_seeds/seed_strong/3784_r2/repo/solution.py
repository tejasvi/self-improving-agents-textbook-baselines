from typing import *


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie; node 0 is root.
        children = [{}]
        depth = [0]
        cnt = [0]
        paths = []  # per word: list of node ids from root (excluding root is fine; include all)
        for w in words:
            cur = 0
            cnt[0] += 1
            path = [0]
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

        # Valid nodes (count >= k), sorted by depth descending.
        valid = [v for v in range(len(children)) if cnt[v] >= k]
        valid.sort(key=lambda v: -depth[v])

        res = [0] * n
        for i in range(n):
            path = paths[i]
            on_path = set(path)
            best = 0
            # Deepest valid node not on path (its count is unchanged by removal).
            for v in valid:
                if v not in on_path:
                    best = depth[v]
                    break
            # Deepest node on path whose count stays >= k after removing word i.
            for v in reversed(path):
                if cnt[v] - 1 >= k:
                    if depth[v] > best:
                        best = depth[v]
                    break
            res[i] = best
        return res
