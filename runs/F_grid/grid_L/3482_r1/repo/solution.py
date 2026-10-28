from typing import List
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Build Aho-Corasick automaton over words (keep min cost per distinct word).
        children = [{}]
        depth = [0]
        cost = [0]  # 0 means no word ends here
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    depth.append(depth[node] + 1)
                    cost.append(0)
                node = nxt
            if cost[node] == 0 or c < cost[node]:
                cost[node] = c

        n_nodes = len(children)
        fail = [0] * n_nodes
        out = [0] * n_nodes  # nearest proper-suffix node (via fail) that is a word end
        queue = deque()
        for ch, nxt in children[0].items():
            fail[nxt] = 0
            queue.append(nxt)
        while queue:
            u = queue.popleft()
            for ch, v in children[u].items():
                f = fail[u]
                while f and ch not in children[f]:
                    f = fail[f]
                fv = children[f].get(ch, 0)
                if fv == v:
                    fv = 0
                fail[v] = fv
                out[v] = fv if cost[fv] else out[fv]
                queue.append(v)

        # Output-chain starting at node: node itself if terminal, else out[node].
        INF = float("inf")
        m = len(target)
        dp = [INF] * (m + 1)
        dp[0] = 0
        state = 0
        for j, ch in enumerate(target):
            while state and ch not in children[state]:
                state = fail[state]
            state = children[state].get(ch, 0)
            v = state if cost[state] else out[state]
            end = j + 1
            best = dp[end]
            while v:
                cand = dp[end - depth[v]] + cost[v]
                if cand < best:
                    best = cand
                v = out[v]
            dp[end] = best

        return -1 if dp[m] == INF else dp[m]
