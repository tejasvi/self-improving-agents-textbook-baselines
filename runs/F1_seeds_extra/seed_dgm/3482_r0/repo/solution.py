from typing import List
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Build trie; keep min cost per distinct word.
        goto = [{}]
        depth = [0]
        cost = [-1]  # cost of word ending at node, -1 if none
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = goto[node].get(ch)
                if nxt is None:
                    nxt = len(goto)
                    goto.append({})
                    depth.append(depth[node] + 1)
                    cost.append(-1)
                    goto[node][ch] = nxt
                node = nxt
            if cost[node] == -1 or c < cost[node]:
                cost[node] = c

        # Build fail links and dictionary links (nearest word-ending proper suffix node).
        n_nodes = len(goto)
        fail = [0] * n_nodes
        dict_link = [0] * n_nodes  # 0 means none (root is never a word end here)
        queue = deque()
        for ch, child in goto[0].items():
            fail[child] = 0
            dict_link[child] = 0
            queue.append(child)
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
                dict_link[v] = fv if cost[fv] != -1 else dict_link[fv]
                queue.append(v)

        INF = float("inf")
        m = len(target)
        dp = [INF] * (m + 1)
        dp[0] = 0
        state = 0
        for j in range(1, m + 1):
            ch = target[j - 1]
            while state and ch not in goto[state]:
                state = fail[state]
            state = goto[state].get(ch, 0)
            node = state if cost[state] != -1 else dict_link[state]
            best = dp[j]
            while node:
                prev = dp[j - depth[node]]
                if prev != INF:
                    cand = prev + cost[node]
                    if cand < best:
                        best = cand
                node = dict_link[node]
            dp[j] = best

        return dp[m] if dp[m] != INF else -1
