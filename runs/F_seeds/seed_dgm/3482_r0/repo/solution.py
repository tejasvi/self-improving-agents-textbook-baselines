from typing import List
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Build trie; store min cost per distinct word at its end node.
        children = [{}]
        depth = [0]
        end_cost = [None]
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    depth.append(depth[node] + 1)
                    end_cost.append(None)
                node = nxt
            if end_cost[node] is None or c < end_cost[node]:
                end_cost[node] = c

        # Aho-Corasick failure links and output links (nearest word-ending suffix node).
        n_nodes = len(children)
        fail = [0] * n_nodes
        out = [0] * n_nodes  # 0 = root = none
        q = deque()
        for ch, v in children[0].items():
            fail[v] = 0
            out[v] = v if end_cost[v] is not None else 0
            q.append(v)
        while q:
            u = q.popleft()
            for ch, v in children[u].items():
                f = fail[u]
                while f and ch not in children[f]:
                    f = fail[f]
                fv = children[f].get(ch, 0)
                if fv == v:
                    fv = 0
                fail[v] = fv
                if end_cost[v] is not None:
                    out[v] = v
                else:
                    out[v] = out[fv]
                q.append(v)

        INF = float("inf")
        m = len(target)
        dp = [INF] * (m + 1)
        dp[0] = 0
        state = 0
        for j in range(1, m + 1):
            ch = target[j - 1]
            while state and ch not in children[state]:
                state = fail[state]
            state = children[state].get(ch, 0)
            v = out[state]
            best = INF
            while v:
                cand = dp[j - depth[v]] + end_cost[v]
                if cand < best:
                    best = cand
                v = out[fail[v]]
            dp[j] = best

        return -1 if dp[m] == INF else dp[m]
