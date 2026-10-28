from typing import *
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Deduplicate words, keeping the cheapest cost for each.
        best = {}
        for w, c in zip(words, costs):
            if w not in best or c < best[w]:
                best[w] = c

        # Build Aho-Corasick automaton over the distinct words.
        goto = [{}]
        fail = [0]
        own = [-1]  # cost of word ending exactly at this node (-1 if none)
        for w, c in best.items():
            node = 0
            for ch in w:
                nxt = goto[node].get(ch)
                if nxt is None:
                    nxt = len(goto)
                    goto.append({})
                    fail.append(0)
                    own.append(-1)
                    goto[node][ch] = nxt
                node = nxt
            own[node] = c

        # BFS to compute failure links and dictionary links.
        # dlink[v] = nearest proper suffix node (via fail chain) that holds a word, or 0.
        dlink = [0] * len(goto)
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
                dlink[v] = fv if own[fv] >= 0 else dlink[fv]
                queue.append(v)

        INF = float("inf")
        n = len(target)
        dp = [INF] * (n + 1)
        dp[0] = 0
        # For each end position j (0-indexed), collect costs of words ending there.
        depth = [0] * len(goto)
        # compute depths via BFS order: depth[v] = depth[u] + 1 along trie edges
        stack = [0]
        while stack:
            u = stack.pop()
            for v in goto[u].values():
                depth[v] = depth[u] + 1
                stack.append(v)

        state = 0
        for j in range(n):
            ch = target[j]
            while state and ch not in goto[state]:
                state = fail[state]
            state = goto[state].get(ch, 0)
            # Walk all words ending at position j.
            v = state if own[state] >= 0 else dlink[state]
            end = j + 1
            while v:
                start = end - depth[v]
                if dp[start] != INF:
                    cand = dp[start] + own[v]
                    if cand < dp[end]:
                        dp[end] = cand
                v = dlink[v]
        return -1 if dp[n] == INF else dp[n]
