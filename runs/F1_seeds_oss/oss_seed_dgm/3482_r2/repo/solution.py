from typing import List
import collections

class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Combine duplicate words keeping the minimal cost
        min_cost = {}
        for w, c in zip(words, costs):
            if w not in min_cost or c < min_cost[w]:
                min_cost[w] = c
        # Build Aho-Corasick trie
        # Each node: dict children, fail link, output list of (word_length, cost)
        trie = [{"next": {}, "fail": 0, "out": []}]  # root index 0
        for w, c in min_cost.items():
            node = 0
            for ch in w:
                nxt = trie[node]["next"].get(ch)
                if nxt is None:
                    nxt = len(trie)
                    trie.append({"next": {}, "fail": 0, "out": []})
                    trie[node]["next"][ch] = nxt
                node = nxt
            trie[node]["out"].append((len(w), c))
        # Build failure links
        queue = collections.deque()
        for ch, nxt in trie[0]["next"].items():
            queue.append(nxt)
            trie[nxt]["fail"] = 0
        while queue:
            v = queue.popleft()
            for ch, nxt in trie[v]["next"].items():
                queue.append(nxt)
                f = trie[v]["fail"]
                while f and ch not in trie[f]["next"]:
                    f = trie[f]["fail"]
                trie[nxt]["fail"] = trie[f]["next"].get(ch, 0)
                # Merge output
                trie[nxt]["out"].extend(trie[trie[nxt]["fail"]]["out"])
        # DP over target
        n = len(target)
        INF = 10**18
        dp = [INF] * (n + 1)
        dp[0] = 0
        node = 0
        for i, ch in enumerate(target):
            # Follow transitions
            while node and ch not in trie[node]["next"]:
                node = trie[node]["fail"]
            node = trie[node]["next"].get(ch, 0)
            # Process outputs ending at position i
            if trie[node]["out"]:
                for length, cost in trie[node]["out"]:
                    start = i - length + 1
                    if start >= 0 and dp[start] != INF:
                        dp[i + 1] = min(dp[i + 1], dp[start] + cost)
        return dp[n] if dp[n] != INF else -1
