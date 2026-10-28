from typing import *
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        n = len(target)
        INF = float('inf')

        # Build trie; keep the cheapest cost for each distinct word.
        goto = [dict()]
        term = [INF]  # minimal cost of word ending exactly at this node
        depth = [0]
        for w, c in zip(words, costs):
            if len(w) > n:
                continue
            node = 0
            for ch in w:
                nxt = goto[node].get(ch)
                if nxt is None:
                    nxt = len(goto)
                    goto.append(dict())
                    term.append(INF)
                    depth.append(depth[node] + 1)
                    goto[node][ch] = nxt
                node = nxt
            if c < term[node]:
                term[node] = c

        m = len(goto)
        fail = [0] * m
        # dict_link[v]: nearest proper suffix node (via fail links) that is terminal, or -1
        dict_link = [-1] * m
        queue = deque()
        for ch, v in goto[0].items():
            fail[v] = 0
            queue.append(v)
        while queue:
            u = queue.popleft()
            for ch, v in goto[u].items():
                f = fail[u]
                while f and ch not in goto[f]:
                    f = fail[f]
                fv = goto[f].get(ch, 0)
                if fv == v:
                    fv = 0
                fail[v] = fv
                fl = fv
                dict_link[v] = fl if term[fl] < INF else dict_link[fl]
                queue.append(v)

        dp = [INF] * (n + 1)
        dp[0] = 0
        state = 0
        for j in range(1, n + 1):
            ch = target[j - 1]
            while state and ch not in goto[state]:
                state = fail[state]
            state = goto[state].get(ch, 0)
            best = INF
            v = state if term[state] < INF else dict_link[state]
            while v > 0:
                # v is terminal (word of length depth(v) ends here)
                # need depth; store lengths via dp index computed from depth
                d = depth[v]
                cand = dp[j - d] + term[v]
                if cand < best:
                    best = cand
                v = dict_link[v]
            dp[j] = best

        return -1 if dp[n] == INF else dp[n]
