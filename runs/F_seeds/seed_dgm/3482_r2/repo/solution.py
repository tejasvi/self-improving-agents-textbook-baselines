from collections import deque
from typing import List


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Build trie; keep cheapest cost for duplicate words.
        children = [{}]
        depth = [0]
        term_cost = [0]  # 0 means not terminal (costs are >= 1)
        for w, c in zip(words, costs):
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    depth.append(depth[node] + 1)
                    term_cost.append(0)
                node = nxt
            if term_cost[node] == 0 or c < term_cost[node]:
                term_cost[node] = c

        n_nodes = len(children)
        fail = [0] * n_nodes
        # dict_link: nearest proper-suffix node (via fail) that is terminal, or -1
        dict_link = [-1] * n_nodes
        goto = children  # will be completed with failure transitions
        queue = deque()
        for ch, nxt in goto[0].items():
            fail[nxt] = 0
            dict_link[nxt] = -1
            queue.append(nxt)
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
                dict_link[v] = fv if term_cost[fv] else dict_link[fv]
                queue.append(v)

        INF = float("inf")
        m = len(target)
        dp = [INF] * (m + 1)
        dp[0] = 0
        node = 0
        for i, ch in enumerate(target):
            while node and ch not in goto[node]:
                node = fail[node]
            node = goto[node].get(ch, 0)
            # enumerate all words ending at position i
            t = node if term_cost[node] else dict_link[node]
            end = i + 1
            while t != -1 and t != 0:
                start = end - depth[t]
                base = dp[start]
                if base != INF:
                    val = base + term_cost[t]
                    if val < dp[end]:
                        dp[end] = val
                t = dict_link[t]
        return dp[m] if dp[m] != INF else -1
