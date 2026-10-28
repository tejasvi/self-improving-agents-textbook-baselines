from typing import *
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        INF = float('inf')
        # Build trie with full goto table (Aho-Corasick).
        goto = [[-1] * 26]
        depth = [0]
        cost = [INF]
        for w, c in zip(words, costs):
            cur = 0
            for ch in w:
                x = ord(ch) - 97
                nxt = goto[cur][x]
                if nxt == -1:
                    nxt = len(goto)
                    goto[cur][x] = nxt
                    goto.append([-1] * 26)
                    depth.append(depth[cur] + 1)
                    cost.append(INF)
                cur = nxt
            if c < cost[cur]:
                cost[cur] = c

        n = len(goto)
        fail = [0] * n
        dlink = [-1] * n  # nearest proper suffix node that is a word end
        q = deque()
        for x in range(26):
            v = goto[0][x]
            if v == -1:
                goto[0][x] = 0
            else:
                fail[v] = 0
                q.append(v)
        while q:
            u = q.popleft()
            fu = fail[u]
            # dlink for u
            dlink[u] = fu if cost[fu] < INF else dlink[fu]
            gu = goto[u]
            gf = goto[fu]
            for x in range(26):
                v = gu[x]
                if v == -1:
                    gu[x] = gf[x]
                else:
                    fail[v] = gf[x]
                    q.append(v)
        # dlink of root children is -1 (root has no cost), handled by default.

        dp = [INF] * (len(target) + 1)
        dp[0] = 0
        state = 0
        for j, ch in enumerate(target):
            state = goto[state][ord(ch) - 97]
            best = dp[j + 1]
            node = state if cost[state] < INF else dlink[state]
            while node > 0:
                cand = dp[j + 1 - depth[node]] + cost[node]
                if cand < best:
                    best = cand
                node = dlink[node]
            dp[j + 1] = best
        return -1 if dp[-1] == INF else dp[-1]
