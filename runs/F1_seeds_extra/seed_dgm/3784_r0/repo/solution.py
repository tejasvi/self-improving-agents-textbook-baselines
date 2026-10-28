from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie with per-node counts of words passing through.
        children = [{}]
        depth = [0]
        cnt = [0]
        paths = []  # node ids for each word, indexed by depth-1
        for w in words:
            node = 0
            cnt[0] += 1
            path = []
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    depth.append(depth[node] + 1)
                    cnt.append(0)
                node = nxt
                cnt[node] += 1
                path.append(node)
            paths.append(path)

        maxd = max(depth) + 1
        size = 1
        while size < maxd:
            size *= 2
        # Segment tree (sum) over depths: count of nodes with cnt >= k at each depth.
        tree = [0] * (2 * size)

        def update(d, delta):
            i = d + size
            while i >= 1:
                tree[i] += delta
                i >>= 1

        def rightmost():
            if tree[1] == 0:
                return 0
            i = 1
            while i < size:
                if tree[2 * i + 1] > 0:
                    i = 2 * i + 1
                else:
                    i = 2 * i
            return i - size

        for v in range(1, len(children)):
            if cnt[v] >= k:
                update(depth[v], 1)

        res = []
        for path in paths:
            # Remove this word: nodes falling below k leave the good set.
            for v in path:
                if cnt[v] == k:
                    update(depth[v], -1)
                cnt[v] -= 1
            res.append(rightmost())
            # Restore.
            for v in path:
                cnt[v] += 1
                if cnt[v] == k:
                    update(depth[v], 1)
        return res
