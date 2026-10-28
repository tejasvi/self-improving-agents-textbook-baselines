from collections import deque
from typing import List


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        INF = float("inf")
        # Build trie with full goto table (Aho-Corasick).
        goto = [[-1] * 26]
        depth = [0]
        cost = [INF]  # min cost of a word ending exactly at this node
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                k = ord(ch) - 97
                nxt = goto[node][k]
                if nxt == -1:
                    nxt = len(goto)
                    goto[node][k] = nxt
                    goto.append([-1] * 26)
                    depth.append(depth[node] + 1)
                    cost.append(INF)
                node = nxt
            if c < cost[node]:
                cost[node] = c

        n_nodes = len(goto)
        fail = [0] * n_nodes
        out = [-1] * n_nodes  # nearest proper fail-ancestor that is a word end
        queue = deque()
        for k in range(26):
            v = goto[0][k]
            if v == -1:
                goto[0][k] = 0
            else:
                fail[v] = 0
                queue.append(v)
        while queue:
            u = queue.popleft()
            fu = fail[u]
            out[u] = fu if cost[fu] < INF else out[fu]
            for k in range(26):
                v = goto[u][k]
                if v == -1:
                    goto[u][k] = goto[fu][k]
                else:
                    fail[v] = goto[fu][k]
                    queue.append(v)

        m = len(target)
        dp = [INF] * (m + 1)
        dp[0] = 0
        state = 0
        for i, ch in enumerate(target):
            state = goto[state][ord(ch) - 97]
            node = state if cost[state] < INF else out[state]
            best = dp[i + 1]
            while node > 0:
                prev = dp[i + 1 - depth[node]]
                if prev != INF:
                    cand = prev + cost[node]
                    if cand < best:
                        best = cand
                node = out[node]
            dp[i + 1] = best
        return -1 if dp[m] == INF else dp[m]
