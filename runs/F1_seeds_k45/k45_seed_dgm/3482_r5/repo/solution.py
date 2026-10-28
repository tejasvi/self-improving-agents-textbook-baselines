from typing import List

class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        """
        Find the minimum cost to construct the target string using given words.
        
        Approach: Dynamic Programming
        - dp[i] = minimum cost to build the first i characters of target
        - For each position i in target, try all words to see if any match at position i
        - If word matches at position i, we can transition from dp[i] to dp[i + len(word)]
        
        Time Complexity: O(n * m * w) where n is len(target), m is len(words), w is avg word length
        Space Complexity: O(n)
        """
        n = len(target)
        # dp[i] represents the minimum cost to build target[0:i]
        dp = [float('inf')] * (n + 1)
        dp[0] = 0  # cost of empty string is 0
        
        # For each position in the target string
        for i in range(n):
            # If this position is not reachable, skip it
            if dp[i] == float('inf'):
                continue
            
            # Try all words to see if any can be appended at position i
            for word, cost in zip(words, costs):
                word_len = len(word)
                # Check if word matches target[i:i+word_len]
                if i + word_len <= n and target[i:i + word_len] == word:
                    # We can use this word, update dp[i + word_len]
                    dp[i + word_len] = min(dp[i + word_len], dp[i] + cost)
        
        # If dp[n] is still infinity, it's impossible to build the target
        return dp[n] if dp[n] != float('inf') else -1
