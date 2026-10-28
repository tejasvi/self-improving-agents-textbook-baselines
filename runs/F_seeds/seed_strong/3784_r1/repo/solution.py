from typing import *


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie: children dicts, count of words through node, depth, representative word.
        children = [{}]
        cnt = [0]
        depth = [0]
        rep = [0]
        for idx, w in enumerate(words):
            node = 0
            cnt[0] += 1
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    cnt.append(0)
                    depth.append(depth[node] + 1)
                    rep.append(idx)
                node = nxt
                cnt[node] += 1

        m = len(children)
        maxdep = max(depth)
        # cntS[d]: number of nodes at depth d with cnt >= k; repS[d]: one such node's rep word index
        cntS = [0] * (maxdep + 1)
        repS = [0] * (maxdep + 1)
        for v in range(m):
            if cnt[v] >= k:
                d = depth[v]
                cntS[d] += 1
                repS[d] = rep[v]

        # D2: deepest level with >= 2 nodes in S (0 if none; root-level handled as 0)
        D2 = 0
        for d in range(maxdep, -1, -1):
            if cntS[d] >= 2:
                D2 = d
                break
        # Deepest level with S nodes is maxS (>= 0 since root in S when n-1>=k).
        maxS = max(d for d in range(maxdep + 1) if cntS[d] > 0)
        L2 = maxS - D2  # chain length beyond D2 (levels with exactly one node)
        # chain bottom node representative: word repS[maxS] prefix of length maxS
        bottom_word = words[repS[maxS]]
        bottom_prefix = bottom_word[:maxS]

        res = [0] * n
        for i, w in enumerate(words):
            # answer1: deepest prefix of w with cnt >= k+1
            node = 0
            best = 0
            for d, ch in enumerate(w, 1):
                node = children[node].get(ch)
                if node is None:
                    break
                if cnt[node] >= k + 1:
                    best = d
                else:
                    break
            # answer2: deepest S node not on w's path
            if L2 > 0 and not w.startswith(bottom_prefix):
                ans2 = maxS
            else:
                ans2 = D2
            res[i] = max(best, ans2)
        return res
