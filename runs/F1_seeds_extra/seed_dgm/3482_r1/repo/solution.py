from collections import deque
from typing import List


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        INF = float("inf")
        # Build Aho-Corasick trie; keep the cheapest cost per distinct word.
        goto = [{}]
        depth = [0]
        term = [INF]  # minimal cost of word ending exactly at node
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = goto[node].get(ch)
                if nxt is None:
                    nxt = len(goto)
                    goto.append({})
                    depth.append(depth[node] + 1)
                    term.append(INF)
                    goto[node][ch] = nxt
                node = nxt
            if c < term[node]:
                term[node] = c

        n_nodes = len(goto)
        fail = [0] * n_nodes
        dict_link = [-1] * n_nodes  # nearest proper suffix node that is a word end
        queue = deque()
        for ch, child in goto[0].items():
            fail[child] = 0
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
                dict_link[v] = fv if term[fv] < INF else dict_link[fv]
                queue.append(v)

        # Transition function filled via fail links for fast scanning.
        def step(state, ch):
            while state and ch not in goto[state]:
                state = fail[state]
            return goto[state].get(ch, 0)

        m = len(target)
        dp = [INF] * (m + 1)
        dp[0] = 0
        state = 0
        for j, ch in enumerate(target):
            state = step(state, ch)
            node = state if term[state] < INF else dict_link[state]
            end = j + 1
            while node > 0:
                start = end - depth[node]
                if dp[start] < INF:
                    cand = dp[start] + term[node]
                    if cand < dp[end]:
                        dp[end] = cand
                node = dict_link[node]
        return dp[m] if dp[m] < INF else -1
