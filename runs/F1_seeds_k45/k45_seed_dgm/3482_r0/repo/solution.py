from typing import List

class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        """
        Find the minimum cost to construct the target string by appending words.
        
        Approach:
        - Use dynamic programming where dp[i] = minimum cost to construct target[0:i]
        - For each position i in target, try all words that could match at position i
        - If target[i-len(word):i] matches a word, update dp[i] = min(dp[i], dp[i-len(word)] + cost)
        - To optimize, for each starting position, group words by their ending position
        - Keep track of the minimum cost among all words that can match at that position
        """
        n = len(target)
        # dp[i] = minimum cost to construct target[0:i]
        dp = [float('inf')] * (n + 1)
        dp[0] = 0  # Empty string costs 0
        
        # For each ending position in target
        for i in range(1, n + 1):
            # Try all words
            for word, cost in zip(words, costs):
                word_len = len(word)
                # Check if this word can be used at position i
                # The word should match target[i-word_len:i]
                if i >= word_len and target[i-word_len:i] == word:
                    # We can use this word if we could construct target[0:i-word_len]
                    if dp[i-word_len] != float('inf'):
                        dp[i] = min(dp[i], dp[i-word_len] + cost)
        
        # If dp[n] is still infinity, it's impossible to construct the target
        return dp[n] if dp[n] != float('inf') else -1
