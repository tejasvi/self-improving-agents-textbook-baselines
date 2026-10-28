from typing import List
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Build trie; keep min cost per distinct word.
        goto = [{}]
        depth = [0]
        term_cost = [None]  # min cost of word ending exactly at node
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

        # Aho-Corasick failure links and dictionary (terminal) links.
        n = len(goto)
        fail = [0] * n
        dict_link = [-1] * n  # nearest proper suffix node that is terminal
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
                dict_link[v] = fv if term_cost[fv] is not None else dict_link[fv]
                queue.append(v)

        INF = float("inf")
        L = len(target)
        dp = [INF] * (L + 1)
        dp[0] = 0
        state = 0
        for j, ch in enumerate(target):
            while state and ch not in goto[state]:
                state = fail[state]
            state = goto[state].get(ch, 0)
            pos = j + 1
            t = state if term_cost[state] is not None else dict_link[state]
            best = dp[pos]
            while t != -1 and t != 0:
                cand = dp[pos - depth[t]] + term_cost[t]
                if cand < best:
                    best = cand
                t = dict_link[t]
            dp[pos] = best

        return -1 if dp[L] == INF else dp[L]
