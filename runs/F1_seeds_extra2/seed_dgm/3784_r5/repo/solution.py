from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie: node 0 is the root.
        children = [{}]
        cnt = [0]
        depth = [0]
        paths = []  # per word: list of node ids along its path (incl. root)
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
                    cnt.append(0)
                    depth.append(depth[cur] + 1)
                cur = nxt
                cnt[cur] += 1
                path.append(cur)
            paths.append(path)

        # Nodes with count >= k, deepest first.
        cand = [v for v in range(len(cnt)) if cnt[v] >= k]
        cand.sort(key=lambda v: -depth[v])

        res = [0] * n
        for i in range(n):
            pathset = set(paths[i])
            ans = 0
            for v in cand:
                # Only path nodes with cnt == k drop below k after removal.
                if cnt[v] == k and v in pathset:
                    continue
                ans = depth[v]
                break
            res[i] = ans
        return res
