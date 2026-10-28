from collections import deque
from typing import List


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        INF = float("inf")

        # Build trie; term_cost[node] = min cost of a word equal to node's string.
        children = [{}]
        depth = [0]
        term_cost = [INF]
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    depth.append(depth[node] + 1)
                    term_cost.append(INF)
                node = nxt
            if c < term_cost[node]:
                term_cost[node] = c

        # Aho-Corasick failure links and dictionary (terminal) suffix links.
        m = len(children)
        fail = [0] * m
        dict_link = [-1] * m  # nearest proper-suffix node that is terminal, or -1
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
                if term_cost[fv] < INF:
                    dict_link[v] = fv
                else:
                    dict_link[v] = dict_link[fv]
                queue.append(v)

        n = len(target)
        dp = [INF] * (n + 1)
        dp[0] = 0
        state = 0
        for i in range(1, n + 1):
            ch = target[i - 1]
            while state and ch not in children[state]:
                state = fail[state]
            state = children[state].get(ch, 0)
            # Enumerate all words that end at position i (suffixes of target[:i]).
            node = state if term_cost[state] < INF else dict_link[state]
            best = INF
            while node != -1:
                cand = dp[i - depth[node]] + term_cost[node]
                if cand < best:
                    best = cand
                node = dict_link[node]
            dp[i] = best

        return -1 if dp[n] == INF else dp[n]
