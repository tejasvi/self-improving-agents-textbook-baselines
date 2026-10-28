from typing import List

class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        n = len(target)
        # dp[i] represents the minimum cost to construct target[0:i]
        # Initialize with infinity, except dp[0] = 0 (empty string costs 0)
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        
        # For each position in the target string
        for i in range(1, n + 1):
            # Check all words
            for word, cost in zip(words, costs):
                word_len = len(word)
                # Check if this word can be used at position i-word_len
                if i >= word_len and target[i - word_len:i] == word:
                    # We can use this word
                    dp[i] = min(dp[i], dp[i - word_len] + cost)
        
        # If dp[n] is still infinity, it's impossible to construct the target
        return dp[n] if dp[n] != float('inf') else -1
