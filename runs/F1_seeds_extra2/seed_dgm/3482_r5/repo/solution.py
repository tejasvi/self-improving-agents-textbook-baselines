from typing import List
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Build a trie; keep the minimum cost for each distinct word.
        children = [{}]
        depth = [0]
        best = [None]  # cost of word ending at node, None if not a word end
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    depth.append(depth[node] + 1)
                    best.append(None)
                node = nxt
            if best[node] is None or c < best[node]:
                best[node] = c

        # Aho-Corasick: failure links and "dictionary" links (nearest proper
        # suffix node that is a word end).
        n = len(children)
        fail = [0] * n
        dict_link = [0] * n  # 0 means none (root is never a word end)
        queue = deque()
        for child in children[0].values():
            queue.append(child)
        while queue:
            u = queue.popleft()
            for ch, v in children[u].items():
                f = fail[u]
                while f and ch not in children[f]:
                    f = fail[f]
                fv = children[f].get(ch, 0)
                fail[v] = fv
                dict_link[v] = fv if best[fv] is not None else dict_link[fv]
                queue.append(v)

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

            # Every word ending at position j is a node on the chain
            # state -> dict_link -> ... (the state itself included).
            node = state if best[state] is not None else dict_link[state]
            cur = INF
            while node:
                prev = dp[j - depth[node]]
                if prev != INF:
                    cand = prev + best[node]
                    if cand < cur:
                        cur = cand
                node = dict_link[node]
            dp[j] = cur

        return -1 if dp[m] == INF else dp[m]
