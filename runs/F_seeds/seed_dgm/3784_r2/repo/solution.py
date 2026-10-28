from typing import List


class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # Build trie; each node stores depth, count of words through it.
        children = [{}]
        depth = [0]
        cnt = [0]
        paths = []  # per word: list of node ids along its path (excluding root)
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

        # Nodes with count >= k, sorted by depth descending.
        good = [v for v in range(len(children)) if v != 0 and cnt[v] >= k]
        good.sort(key=lambda v: -depth[v])

        res = [0] * n
        if n - 1 < k:
            return res
        for i, path in enumerate(paths):
            best = 0
            pathset = set(path)
            # Nodes on the path remain valid only if count-1 >= k.
            for v in path:
                if cnt[v] >= k + 1 and depth[v] > best:
                    best = depth[v]
            # Nodes off the path keep their count; take deepest such node.
            for v in good:
                if v not in pathset:
                    if depth[v] > best:
                        best = depth[v]
                    break
            res[i] = best
        return res
