from typing import *
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        n = len(target)
        INF = float('inf')

        # Trie over words; term[node] = min cost of a word ending at node (-1 if none).
        children: List[Dict[str, int]] = [{}]
        term: List[int] = [-1]
        depth: List[int] = [0]
        for w, c in zip(words, costs):
            if len(w) > n:
                continue
            cur = 0
            for ch in w:
                nxt = children[cur].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[cur][ch] = nxt
                    children.append({})
                    term.append(-1)
                    depth.append(depth[cur] + 1)
                cur = nxt
            if term[cur] == -1 or c < term[cur]:
                term[cur] = c

        m = len(children)
        if m == 1:
            return -1

        # Aho-Corasick: fail links, and dlink = nearest proper suffix node that is terminal.
        fail = [0] * m
        dlink = [-1] * m
        order = deque()
        for v in children[0].values():
            order.append(v)
        while order:
            u = order.popleft()
            for ch, v in children[u].items():
                f = fail[u]
                while f and ch not in children[f]:
                    f = fail[f]
                fv = children[f].get(ch, 0)
                if fv == v:  # only possible when u is root
                    fv = 0
                fail[v] = fv
                dlink[v] = fv if term[fv] != -1 else dlink[fv]
                order.append(v)

        # dp[j] = min cost to build target[:j].
        dp = [INF] * (n + 1)
        dp[0] = 0
        state = 0
        for j in range(1, n + 1):
            ch = target[j - 1]
            while state and ch not in children[state]:
                state = fail[state]
            state = children[state].get(ch, 0)
            best = INF
            v = state if term[state] != -1 else dlink[state]
            while v != -1:
                cand = dp[j - depth[v]] + term[v]
                if cand < best:
                    best = cand
                v = dlink[v]
            dp[j] = best
        return -1 if dp[n] == INF else dp[n]
