from typing import List

class TrieNode:
    __slots__ = ("children", "cost")
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        # Minimum cost of any word ending at this node; None if no word ends here
        self.cost: int | None = None

class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        """Return the minimum total cost to form *target* by concatenating
        strings from *words* (each used any number of times) with respective
        *costs*. If impossible, return -1.

        The classic solution is a DP over prefixes of ``target`` combined with a
        Trie that stores all ``words``. ``dp[i]`` stores the cheapest cost to
        build ``target[:i]``. For each reachable position ``i`` we walk the Trie
        character by character starting at ``target[i]``; whenever we reach a
        node that marks the end of a word we can update ``dp`` for the position
        after that word.
        """
        n = len(target)
        # Build Trie with the minimum cost for duplicate words
        root = TrieNode()
        for w, c in zip(words, costs):
            node = root
            for ch in w:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            # Keep the cheapest cost for this exact word
            if node.cost is None or c < node.cost:
                node.cost = c

        INF = 10 ** 18
        dp = [INF] * (n + 1)
        dp[0] = 0
        for i in range(n):
            if dp[i] == INF:
                continue
            node = root
            # Attempt to match any word starting at position i
            for j in range(i, n):
                ch = target[j]
                if ch not in node.children:
                    break
                node = node.children[ch]
                if node.cost is not None:
                    nxt = j + 1
                    new_cost = dp[i] + node.cost
                    if new_cost < dp[nxt]:
                        dp[nxt] = new_cost
        return dp[n] if dp[n] != INF else -1
