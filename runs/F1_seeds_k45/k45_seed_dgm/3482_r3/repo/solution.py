class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        """
        Find the minimum cost to construct the target string by appending words.
        
        Approach:
        - Use dynamic programming where dp[i] represents the minimum cost to 
          construct target[0:i]
        - For each position i in target, try all words that can match at this position
        - If a word matches, update dp[i + len(word)] with the minimum cost
        
        Time Complexity: O(n * m * k) where n is target length, m is number of words,
                        k is average word length
        Space Complexity: O(n) for the dp array
        """
        n = len(target)
        # dp[i] = minimum cost to construct target[0:i]
        # Initialize with infinity, except dp[0] = 0 (empty string costs 0)
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        
        # For each position in the target string
        for i in range(n):
            # Skip if this position is unreachable
            if dp[i] == float('inf'):
                continue
            
            # Try all words
            for word, cost in zip(words, costs):
                word_len = len(word)
                # Check if the word can fit and matches at position i
                if i + word_len <= n and target[i:i + word_len] == word:
                    # Update the cost to reach position i + word_len
                    dp[i + word_len] = min(dp[i + word_len], dp[i] + cost)
        
        # If dp[n] is still infinity, it's impossible to construct the target
        return dp[n] if dp[n] != float('inf') else -1
