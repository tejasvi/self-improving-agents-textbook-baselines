from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie: children dicts, count of words through each node, depth.
        children = [{}]
        cnt = [0]
        depth = [0]
        paths = []  # paths[i][d-1] = node id at depth d for word i
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

        # Shared nodes (cnt >= k) grouped by depth.
        cnt_s = {}
        for v in range(1, len(cnt)):
            if cnt[v] >= k:
                d = depth[v]
                cnt_s[d] = cnt_s.get(d, 0) + 1
        ds = sorted(cnt_s.keys(), reverse=True)  # distinct shared depths, desc

        ans = [0] * n
        for i in range(n):
            path = paths[i]
            plen = len(path)
            best = 0
            # Candidate from nodes on path i that still have count >= k after removal.
            for d in range(plen, 0, -1):
                if cnt[path[d - 1]] >= k + 1:
                    best = d
                    break
            # Candidate from shared nodes off path i (deepest first).
            for d in ds:
                if d <= plen:
                    on = 1 if cnt[path[d - 1]] >= k else 0
                else:
                    on = 0
                if cnt_s[d] - on > 0:
                    if d > best:
                        best = d
                    break
            ans[i] = best
        return ans
