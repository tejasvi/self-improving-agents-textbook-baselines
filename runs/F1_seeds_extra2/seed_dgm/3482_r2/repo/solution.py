from typing import List
from collections import deque


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        INF = float("inf")

        # Build a trie over the words, keeping the cheapest cost per word.
        children = [{}]
        depth = [0]
        end_cost = [INF]
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    depth.append(depth[node] + 1)
                    end_cost.append(INF)
                node = nxt
            if c < end_cost[node]:
                end_cost[node] = c

        # Aho-Corasick: failure links and dictionary links (nearest proper
        # suffix node that terminates a word; -1 if none).
        m = len(children)
        fail = [0] * m
        dict_link = [-1] * m
        goto = children
        q = deque(goto[0].values())
        while q:
            u = q.popleft()
            for ch, v in goto[u].items():
                f = fail[u]
                while f and ch not in goto[f]:
                    f = fail[f]
                fv = goto[f].get(ch, 0)
                if fv == v:
                    fv = 0
                fail[v] = fv
                dict_link[v] = fv if end_cost[fv] < INF else dict_link[fv]
                q.append(v)

        n = len(target)
        # Scan target once to find the automaton state after each prefix.
        states = [0] * (n + 1)
        state = 0
        for j, ch in enumerate(target, 1):
            s = state
            while s and ch not in goto[s]:
                s = fail[s]
            state = goto[s].get(ch, 0)
            states[j] = state

        # dp[j] = min cost to build target[:j].
        # Every word ending at position j is a node on the suffix/dictionary
        # chain of states[j]; each such word has length depth[node].
        dp = [INF] * (n + 1)
        dp[0] = 0
        for j in range(1, n + 1):
            s = states[j]
            u = s if end_cost[s] < INF else dict_link[s]
            best = INF
            while u > 0:
                cand = dp[j - depth[u]] + end_cost[u]
                if cand < best:
                    best = cand
                u = dict_link[u]
                if u == -1:
                    break
            dp[j] = best
        return dp[n] if dp[n] < INF else -1
