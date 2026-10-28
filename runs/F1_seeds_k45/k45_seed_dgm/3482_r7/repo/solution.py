from typing import List

class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        """
        Find the minimum cost to construct the target string by appending words.
        
        Args:
            target: The target string to construct
            words: List of available words to append
            costs: Cost associated with each word
            
        Returns:
            Minimum cost to construct target, or -1 if impossible
        """
        n = len(target)
        
        # dp[i] = minimum cost to construct target[0:i]
        # Initialize with infinity, except dp[0] = 0 (empty string costs 0)
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        
        # For each position in the target
        for i in range(n):
            # If we can't reach position i, skip
            if dp[i] == float('inf'):
                continue
            
            # Try each word
            for word, cost in zip(words, costs):
                word_len = len(word)
                
                # Check if the word matches at position i
                if i + word_len <= n and target[i:i + word_len] == word:
                    # Update the cost at the new position
                    dp[i + word_len] = min(dp[i + word_len], dp[i] + cost)
        
        # If dp[n] is still infinity, it's impossible to construct the target
        return dp[n] if dp[n] != float('inf') else -1
