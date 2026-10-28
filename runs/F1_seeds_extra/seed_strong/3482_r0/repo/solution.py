from typing import *
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        INF = float("inf")
        # Build trie; keep the cheapest cost for each distinct word.
        children = [dict()]
        depth = [0]
        wcost = [INF]  # min cost of a word ending exactly at this node
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append(dict())
                    depth.append(depth[node] + 1)
                    wcost.append(INF)
                node = nxt
            if c < wcost[node]:
                wcost[node] = c

        m = len(children)
        fail = [0] * m
        # dictionary link: nearest proper suffix node that is a word end
        dlink = [-1] * m
        # full goto transitions per node (computed in BFS order)
        goto = [None] * m
        goto[0] = dict(children[0])
        queue = deque()
        for ch, nxt in children[0].items():
            fail[nxt] = 0
            dlink[nxt] = -1
            queue.append(nxt)
        while queue:
            u = queue.popleft()
            fu = fail[u]
            # full transitions for u
            g = dict(goto[fu])
            g.update(children[u])
            goto[u] = g
            for ch, v in children[u].items():
                fv = goto[fu].get(ch, 0) if u != 0 else 0
                fail[v] = fv
                dlink[v] = fv if wcost[fv] < INF else dlink[fv]
                queue.append(v)

        n = len(target)
        dp = [INF] * (n + 1)
        dp[0] = 0
        state = 0
        for j in range(1, n + 1):
            state = goto[state].get(target[j - 1], 0)
            best = INF
            v = state if wcost[state] < INF else dlink[state]
            while v > 0:
                cand = dp[j - depth[v]] + wcost[v]
                if cand < best:
                    best = cand
                v = dlink[v]
            dp[j] = best
        return -1 if dp[n] == INF else dp[n]
