from collections import deque
from typing import List


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        INF = float("inf")
        # Build Aho-Corasick trie; keep min cost per distinct word.
        goto = [{}]
        depth = [0]
        cost = [INF]  # min cost of word ending exactly at node
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = goto[node].get(ch)
                if nxt is None:
                    nxt = len(goto)
                    goto.append({})
                    depth.append(depth[node] + 1)
                    cost.append(INF)
                    goto[node][ch] = nxt
                node = nxt
            if c < cost[node]:
                cost[node] = c

        n_nodes = len(goto)
        fail = [0] * n_nodes
        # dict_link: nearest proper suffix node that has a word ending there
        dict_link = [-1] * n_nodes
        queue = deque()
        for ch, nxt in goto[0].items():
            fail[nxt] = 0
            queue.append(nxt)
        # dict_link of depth-1 nodes is root (-1 = none)
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
                dict_link[v] = fv if cost[fv] < INF else dict_link[fv]
                queue.append(v)

        # Transition function is computed on the fly via fail links.
        m = len(target)
        dp = [INF] * (m + 1)
        dp[0] = 0
        state = 0
        for i in range(m):
            ch = target[i]
            while state and ch not in goto[state]:
                state = fail[state]
            state = goto[state].get(ch, 0)
            v = state if cost[state] < INF else dict_link[state]
            best = dp[i + 1]
            while v > 0:
                cand = dp[i + 1 - depth[v]] + cost[v]
                if cand < best:
                    best = cand
                v = dict_link[v] if dict_link[v] != -1 else 0
            dp[i + 1] = best
        return -1 if dp[m] == INF else dp[m]
