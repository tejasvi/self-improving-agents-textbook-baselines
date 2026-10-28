from typing import *


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie; cnt[node] = number of words passing through node.
        children = [{}]
        depth = [0]
        cnt = [0]
        paths = []  # node ids along each word's path (excluding root)
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

        # Active nodes: cnt >= k (depth > 0). Count them per depth.
        m = len(children)
        cnt_depth = {}
        for v in range(1, m):
            if cnt[v] >= k:
                d = depth[v]
                cnt_depth[d] = cnt_depth.get(d, 0) + 1
        dens = sorted(cnt_depth.keys(), reverse=True)

        res = [0] * n
        for i in range(n):
            dec = {}
            for v in paths[i]:
                # After removing word i, a node is still active iff cnt-1 >= k.
                if cnt[v] == k:
                    d = depth[v]
                    dec[d] = dec.get(d, 0) + 1
            ans = 0
            for d in dens:
                if cnt_depth[d] - dec.get(d, 0) > 0:
                    ans = d
                    break
            res[i] = ans
        return res
