from collections import deque
from typing import List


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Aho-Corasick automaton over the words; keep the cheapest cost per distinct word.
        goto = [{}]
        depth = [0]
        term_cost = [None]  # cheapest cost of a word ending exactly at this node
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = goto[node].get(ch)
                if nxt is None:
                    nxt = len(goto)
                    goto[node][ch] = nxt
                    goto.append({})
                    depth.append(depth[node] + 1)
                    term_cost.append(None)
                node = nxt
            if term_cost[node] is None or c < term_cost[node]:
                term_cost[node] = c

        m = len(goto)
        fail = [0] * m
        # dict_link[v]: nearest proper suffix node of v (via fail links) that is terminal, or -1
        dict_link = [-1] * m
        queue = deque()
        for v in goto[0].values():
            queue.append(v)
        while queue:
            u = queue.popleft()
            for ch, v in goto[u].items():
                f = fail[u]
                while f and ch not in goto[f]:
                    f = fail[f]
                fv = goto[f].get(ch, 0)
                if fv == v:  # only possible for root children
                    fv = 0
                fail[v] = fv
                dict_link[v] = fv if term_cost[fv] is not None else dict_link[fv]
                queue.append(v)

        INF = float("inf")
        n = len(target)
        dp = [INF] * (n + 1)
        dp[0] = 0
        node = 0
        for i, ch in enumerate(target):
            while node and ch not in goto[node]:
                node = fail[node]
            node = goto[node].get(ch, 0)
            end = i + 1
            # Every word ending at position `end` is a terminal node on the
            # suffix chain of `node`.
            v = node if term_cost[node] is not None else dict_link[node]
            best = INF
            while v != -1:
                start = end - depth[v]
                cand = dp[start] + term_cost[v]
                if cand < best:
                    best = cand
                v = dict_link[v]
            dp[end] = best

        return -1 if dp[n] == INF else dp[n]
