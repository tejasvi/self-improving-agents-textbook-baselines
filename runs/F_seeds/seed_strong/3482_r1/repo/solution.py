from typing import *
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        INF = float("inf")
        # Build trie. goto[node*26 + c] -> child (or -1 before fail completion)
        goto = [-1] * 26
        depth = [0]
        cost_at = [INF]
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                k = ord(ch) - 97
                nxt = goto[node * 26 + k]
                if nxt == -1:
                    nxt = len(depth)
                    goto.extend([-1] * 26)
                    depth.append(depth[node] + 1)
                    cost_at.append(INF)
                    goto[node * 26 + k] = nxt
                node = nxt
            if c < cost_at[node]:
                cost_at[node] = c

        n_nodes = len(depth)
        fail = [0] * n_nodes
        dict_link = [0] * n_nodes  # nearest proper suffix node that is a word end (0 = none)
        q = deque()
        for k in range(26):
            v = goto[k]
            if v == -1:
                goto[k] = 0
            else:
                fail[v] = 0
                dict_link[v] = 0
                q.append(v)
        while q:
            u = q.popleft()
            fu = fail[u]
            for k in range(26):
                idx = u * 26 + k
                v = goto[idx]
                if v == -1:
                    goto[idx] = goto[fu * 26 + k]
                else:
                    f = goto[fu * 26 + k]
                    fail[v] = f
                    dict_link[v] = f if cost_at[f] < INF else dict_link[f]
                    q.append(v)

        m = len(target)
        dp = [INF] * (m + 1)
        dp[0] = 0
        state = 0
        for j in range(m):
            state = goto[state * 26 + ord(target[j]) - 97]
            best = INF
            v = state if cost_at[state] < INF else dict_link[state]
            # v == 0 means root (never a word end), so loop stops
            while v:
                cand = dp[j + 1 - depth[v]] + cost_at[v]
                if cand < best:
                    best = cand
                v = dict_link[v]
            dp[j + 1] = best
        return -1 if dp[m] == INF else dp[m]
