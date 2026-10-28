from typing import *
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Build Aho-Corasick automaton over words (keep min cost per distinct word).
        INF = float('inf')
        best_word = {}
        for w, c in zip(words, costs):
            if w not in best_word or c < best_word[w]:
                best_word[w] = c

        goto = [[-1] * 26]
        depth = [0]
        endcost = [0]  # 0 means no word ends here (costs >= 1)
        for w, c in best_word.items():
            node = 0
            for ch in w:
                k = ord(ch) - 97
                nxt = goto[node][k]
                if nxt == -1:
                    nxt = len(goto)
                    goto.append([-1] * 26)
                    depth.append(depth[node] + 1)
                    endcost.append(0)
                    goto[node][k] = nxt
                node = nxt
            endcost[node] = c

        n = len(goto)
        fail = [0] * n
        # out[v]: nearest node on fail chain (excluding v) that is a word end, or -1
        out = [-1] * n
        dq = deque()
        for k in range(26):
            v = goto[0][k]
            if v == -1:
                goto[0][k] = 0
            else:
                fail[v] = 0
                dq.append(v)
        while dq:
            u = dq.popleft()
            fu = fail[u]
            out[u] = fu if endcost[fu] else out[fu]
            gu = goto[u]
            gf = goto[fu]
            for k in range(26):
                v = gu[k]
                if v == -1:
                    gu[k] = gf[k]
                else:
                    fail[v] = gf[k]
                    dq.append(v)
        # out for depth-1 nodes: fail is root (endcost[0]=0), out=-1 already correct.

        m = len(target)
        dp = [INF] * (m + 1)
        dp[0] = 0
        state = 0
        for j in range(1, m + 1):
            state = goto[state][ord(target[j - 1]) - 97]
            best = INF
            v = state if endcost[state] else out[state]
            while v > 0:
                cand = dp[j - depth[v]] + endcost[v]
                if cand < best:
                    best = cand
                v = out[v]
            dp[j] = best
        return -1 if dp[m] == INF else dp[m]
