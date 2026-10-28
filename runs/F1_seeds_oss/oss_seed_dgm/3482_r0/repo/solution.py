"""Solution for minimum cost string construction.
We use an Aho-Corasick automaton to find all occurrences of the given words in the target string.
For each occurrence ending at position i, we can update dp[i] = min(dp[i], dp[i - len(word)] + cost).
The answer is dp[len(target)] or -1 if unreachable.
"""

from typing import List, Dict, Deque
from collections import deque


class Node:
    __slots__ = ("children", "fail", "outputs")

    def __init__(self):
        self.children: Dict[str, "Node"] = {}
        self.fail: "Node" = None  # type: ignore
        # each output is a tuple (length of word, cost)
        self.outputs: List[tuple[int, int]] = []


class AhoCorasick:
    def __init__(self):
        self.root = Node()
        self.root.fail = self.root

    def add_word(self, word: str, cost: int):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Node()
            node = node.children[ch]
        # Keep only minimal cost for the same word length (words are unique strings after preprocessing)
        node.outputs.append((len(word), cost))

    def build(self):
        q: Deque[Node] = deque()
        # Initialize fail links of depth 1 nodes to root
        for child in self.root.children.values():
            child.fail = self.root
            q.append(child)
        # BFS
        while q:
            current = q.popleft()
            for ch, nxt in current.children.items():
                # compute fail for nxt
                fail_node = current.fail
                while fail_node is not self.root and ch not in fail_node.children:
                    fail_node = fail_node.fail
                nxt.fail = fail_node.children.get(ch, self.root) if ch in fail_node.children else self.root
                # merge output
                nxt.outputs.extend(nxt.fail.outputs)
                q.append(nxt)

    def iter_matches(self, text: str):
        """Yield (end_position (1‑based), word_length, cost) for each match.
        end_position is the index in text after the matched word (i.e., dp index).
        """
        node = self.root
        for idx, ch in enumerate(text):
            while node is not self.root and ch not in node.children:
                node = node.fail
            node = node.children.get(ch, self.root)
            if node.outputs:
                for length, cost in node.outputs:
                    yield idx + 1, length, cost


class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Preprocess duplicate words, keep minimal cost for each distinct word
        best_cost: Dict[str, int] = {}
        for w, c in zip(words, costs):
            if w not in best_cost or c < best_cost[w]:
                best_cost[w] = c

        # Build automaton
        ac = AhoCorasick()
        for w, c in best_cost.items():
            ac.add_word(w, c)
        ac.build()

        n = len(target)
        INF = 10 ** 18
        dp = [INF] * (n + 1)
        dp[0] = 0

        # Iterate through text, updating dp when matches end at position i
        for end_pos, length, cost in ac.iter_matches(target):
            start = end_pos - length
            if dp[start] + cost < dp[end_pos]:
                dp[end_pos] = dp[start] + cost

        return dp[n] if dp[n] != INF else -1
