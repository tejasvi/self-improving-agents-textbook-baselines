from typing import List
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        INF = float("inf")

        # Build trie; store minimum cost for each word ending at a node.
        children = [{}]
        depth = [0]
        cost_at = [INF]
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    depth.append(depth[node] + 1)
                    cost_at.append(INF)
                node = nxt
            if c < cost_at[node]:
                cost_at[node] = c

        # Aho-Corasick failure links and output links (nearest proper suffix
        # node that is a word end).
        m = len(children)
        fail = [0] * m
        out = [-1] * m  # output link: node index or -1
        queue = deque()
        for ch, nxt in children[0].items():
            fail[nxt] = 0
            queue.append(nxt)
        while queue:
            u = queue.popleft()
            for ch, v in children[u].items():
                f = fail[u]
                while f and ch not in children[f]:
                    f = fail[f]
                fv = children[f].get(ch, 0)
                if fv == v:
                    fv = 0
                fail[v] = fv
                out[v] = fv if cost_at[fv] < INF else out[fv]
                queue.append(v)

        n = len(target)
        dp = [INF] * (n + 1)
        dp[0] = 0
        state = 0
        for j in range(1, n + 1):
            ch = target[j - 1]
            while state and ch not in children[state]:
                state = fail[state]
            state = children[state].get(ch, 0)
            best = dp[j]
            v = state if cost_at[state] < INF else out[state]
            while v != -1 and v != 0:
                prev = dp[j - depth[v]]
                if prev != INF:
                    cand = prev + cost_at[v]
                    if cand < best:
                        best = cand
                v = out[v]
            dp[j] = best

        return -1 if dp[n] == INF else dp[n]
