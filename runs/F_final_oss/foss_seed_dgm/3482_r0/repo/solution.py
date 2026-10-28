from typing import List

class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Reduce duplicate words by keeping minimal cost
        min_cost = {}
        for w, c in zip(words, costs):
            if w not in min_cost or c < min_cost[w]:
                min_cost[w] = c

        # Build a trie for the words with their minimal cost
        class Node:
            __slots__ = ("children", "cost")
            def __init__(self):
                self.children = {}
                self.cost = None  # cost of word ending at this node

        root = Node()
        for w, c in min_cost.items():
            node = root
            for ch in w:
                if ch not in node.children:
                    node.children[ch] = Node()
                node = node.children[ch]
            # store the minimal cost for this word
            node.cost = c

        n = len(target)
        INF = 10**18
        dp = [INF] * (n + 1)
        dp[0] = 0

        for i in range(n):
            if dp[i] == INF:
                continue
            node = root
            j = i
            while j < n:
                ch = target[j]
                if ch not in node.children:
                    break
                node = node.children[ch]
                j += 1
                if node.cost is not None:
                    new_cost = dp[i] + node.cost
                    if new_cost < dp[j]:
                        dp[j] = new_cost
        return dp[n] if dp[n] != INF else -1
