from typing import List

class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        # Preprocess: keep only the cheapest cost for each distinct word
        min_cost = {}
        for w, c in zip(words, costs):
            if w in min_cost:
                if c < min_cost[w]:
                    min_cost[w] = c
            else:
                min_cost[w] = c
        # Build Aho-Corasick automaton
        # Each node: dict next, fail link, output list of (word_len, cost)
        class Node:
            __slots__ = ('next', 'fail', 'out')
            def __init__(self):
                self.next = {}
                self.fail = None
                self.out = []  # list of (length, cost)
        root = Node()
        # Insert words
        for w, c in min_cost.items():
            node = root
            for ch in w:
                if ch not in node.next:
                    node.next[ch] = Node()
                node = node.next[ch]
            node.out.append((len(w), c))
        # Build failure links using BFS
        from collections import deque
        q = deque()
        # Initialize root's children fail to root
        for ch, nxt in root.next.items():
            nxt.fail = root
            q.append(nxt)
        root.fail = root  # root fails to itself
        while q:
            cur = q.popleft()
            for ch, nxt in cur.next.items():
                # set fail for nxt
                fail_node = cur.fail
                while fail_node is not root and ch not in fail_node.next:
                    fail_node = fail_node.fail
                nxt.fail = fail_node.next.get(ch, root) if ch in fail_node.next else root
                # merge output
                nxt.out.extend(nxt.fail.out)
                q.append(nxt)
        # DP over target
        n = len(target)
        INF = 10**18
        dp = [INF] * (n + 1)
        dp[0] = 0
        node = root
        for i, ch in enumerate(target):
            # Follow transitions, using fail links as needed
            while node is not root and ch not in node.next:
                node = node.fail
            if ch in node.next:
                node = node.next[ch]
            else:
                node = root
            # Process all words ending at position i
            if node.out:
                for length, cost in node.out:
                    start = i - length + 1
                    if start >= 0 and dp[start] != INF:
                        dp[i+1] = min(dp[i+1], dp[start] + cost)
        return -1 if dp[n] == INF else dp[n]
