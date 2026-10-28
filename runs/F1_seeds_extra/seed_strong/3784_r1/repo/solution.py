from typing import *


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # Build trie: children, count of words through node, depth.
        children = [{}]
        cnt = [0]
        depth = [0]
        for w in words:
            cur = 0
            cnt[0] += 1
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

        # Nodes (excluding root) with cnt >= k, sorted by depth descending.
        good = [v for v in range(1, len(cnt)) if cnt[v] >= k]
        good.sort(key=lambda v: -depth[v])

        ans = [0] * n
        for i, w in enumerate(words):
            if n - 1 < k:
                ans[i] = 0
                continue
            # Path nodes of word i (root excluded).
            path = []
            cur = 0
            for ch in w:
                cur = children[cur][ch]
                path.append(cur)
            best = 0
            # Deepest path node still having >= k words after removal.
            for v in reversed(path):
                if cnt[v] - 1 >= k:
                    best = max(best, depth[v])
                    break
            # Deepest non-path node with cnt >= k.
            onpath = set(path)
            for v in good:
                if v not in onpath:
                    best = max(best, depth[v])
                    break
            ans[i] = best
        return ans
