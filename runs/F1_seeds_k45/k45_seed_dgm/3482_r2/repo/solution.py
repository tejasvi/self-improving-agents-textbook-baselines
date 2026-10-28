from typing import List

class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        """
        Find the minimum cost to construct the target string using words with given costs.
        
        Approach:
        - Use dynamic programming where dp[i] = minimum cost to build target[0:i]
        - For each position i, try to match each word starting at that position
        - If word matches, update dp[i + len(word)] with minimum cost
        
        Time Complexity: O(n * m * k) where n = len(target), m = len(words), k = avg word length
        Space Complexity: O(n) for the dp array
        """
        n = len(target)
        # dp[i] = minimum cost to build target[0:i]
        dp = [float('inf')] * (n + 1)
        dp[0] = 0  # Base case: empty string costs 0
        
        # For each position in target
        for i in range(n):
            # If we can't reach position i, skip
            if dp[i] == float('inf'):
                continue
            
            # Try each word
            for word, cost in zip(words, costs):
                word_len = len(word)
                # Check if word can be placed at position i
                if i + word_len <= n and target[i:i + word_len] == word:
                    # Update the position after this word
                    dp[i + word_len] = min(dp[i + word_len], dp[i] + cost)
        
        # If dp[n] is still infinity, it's impossible to build target
        return dp[n] if dp[n] != float('inf') else -1
