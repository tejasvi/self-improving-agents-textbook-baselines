from typing import *
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        INF = float('inf')
        # Build trie; keep min cost per distinct word.
        goto = [{}]
        depth = [0]
        best = [INF]  # min cost of word ending at node
        for w, c in zip(words, costs):
            if len(w) > len(target):
                continue
            v = 0
            for ch in w:
                nxt = goto[v].get(ch)
                if nxt is None:
                    nxt = len(goto)
                    goto.append({})
                    depth.append(depth[v] + 1)
                    best.append(INF)
                    goto[v][ch] = nxt
                v = nxt
            if c < best[v]:
                best[v] = c
        n_nodes = len(goto)
        if n_nodes == 1:
            return -1
        fail = [0] * n_nodes
        # term_link[v]: nearest node on suffix-link chain (including v) that is terminal
        term_link = [0] * n_nodes
        # BFS
        order = deque(goto[0].values())  # root children have fail 0
        while order:
            v = order.popleft()
            term_link[v] = v if best[v] < INF else term_link[fail[v]]
            for ch, u in goto[v].items():
                f = fail[v]
                while f and ch not in goto[f]:
                    f = fail[f]
                nf = goto[f].get(ch, 0)
                fail[u] = nf if nf != u else 0
                order.append(u)

        m = len(target)
        dp = [INF] * (m + 1)
        dp[0] = 0
        v = 0
        for j in range(m):
            ch = target[j]
            while v and ch not in goto[v]:
                v = fail[v]
            v = goto[v].get(ch, 0)
            u = term_link[v]
            end = j + 1
            while u:
                cand = dp[end - depth[u]] + best[u]
                if cand < dp[end]:
                    dp[end] = cand
                u = term_link[fail[u]]
        return dp[m] if dp[m] < INF else -1
