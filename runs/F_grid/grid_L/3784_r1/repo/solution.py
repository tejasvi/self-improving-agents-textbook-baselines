from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        # Build trie: child maps, depth and number of words through each node.
        children = [{}]
        depth = [0]
        cnt = [0]
        paths = []
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

        maxd = max(depth)
        size = 1
        while size < maxd + 1:
            size <<= 1
        tree = [0] * (2 * size)

        def update(d, delta):
            p = d + size
            while p:
                tree[p] += delta
                p >>= 1

        # Mark nodes with cnt >= k as good in the depth segment tree.
        for v in range(len(children)):
            if cnt[v] >= k:
                update(depth[v], 1)

        def query():
            if tree[1] == 0:
                return 0
            node = 1
            while node < size:
                if tree[2 * node + 1] > 0:
                    node = 2 * node + 1
                else:
                    node = 2 * node
            return node - size

        res = [0] * n
        for i in range(n):
            path = paths[i]
            # Remove word i: decrement counts along its path.
            for v in path:
                if cnt[v] == k:
                    update(depth[v], -1)
                cnt[v] -= 1
            res[i] = query()
            # Restore.
            for v in path:
                cnt[v] += 1
                if cnt[v] == k:
                    update(depth[v], 1)
        return res
