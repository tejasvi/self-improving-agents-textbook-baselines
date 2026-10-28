from collections import deque
from typing import List


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Keep the cheapest cost for each distinct word.
        best = {}
        for w, c in zip(words, costs):
            if w not in best or c < best[w]:
                best[w] = c

        # Build an Aho-Corasick automaton over the words.
        goto = [{}]
        fail = [0]
        depth = [0]
        out_cost = [-1]   # cost of a word ending exactly at this node, -1 if none
        out_link = [-1]   # nearest proper suffix node that ends a word, -1 if none
        for w, c in best.items():
            node = 0
            for ch in w:
                nxt = goto[node].get(ch)
                if nxt is None:
                    nxt = len(goto)
                    goto.append({})
                    fail.append(0)
                    depth.append(depth[node] + 1)
                    out_cost.append(-1)
                    out_link.append(-1)
                    goto[node][ch] = nxt
                node = nxt
            out_cost[node] = c

        # BFS to compute failure links and output links.
        queue = deque()
        for nxt in goto[0].values():
            fail[nxt] = 0
            queue.append(nxt)
        while queue:
            u = queue.popleft()
            for ch, v in goto[u].items():
                f = fail[u]
                while f and ch not in goto[f]:
                    f = fail[f]
                fv = goto[f].get(ch, 0)
                fail[v] = fv
                out_link[v] = fv if out_cost[fv] >= 0 else out_link[fv]
                queue.append(v)

        INF = float("inf")
        n = len(target)
        dp = [INF] * (n + 1)
        dp[0] = 0
        state = 0
        for j, ch in enumerate(target):
            while state and ch not in goto[state]:
                state = fail[state]
            state = goto[state].get(ch, 0)

            # Enumerate every word that ends at position j (a suffix of target[:j+1]).
            end = j + 1
            node = state if out_cost[state] >= 0 else out_link[state]
            while node > 0:
                start = end - depth[node]
                if dp[start] != INF:
                    cand = dp[start] + out_cost[node]
                    if cand < dp[end]:
                        dp[end] = cand
                node = out_link[node]

        return -1 if dp[n] == INF else dp[n]
