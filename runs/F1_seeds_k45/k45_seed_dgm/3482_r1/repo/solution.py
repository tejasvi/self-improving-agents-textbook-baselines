class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        """
        Find the minimum cost to construct the target string using given words.
        
        Approach:
        - Use dynamic programming where dp[i] represents the minimum cost to build
          the first i characters of the target string
        - For each position i, try all words to see if they match starting at position i
        - If a word matches, update dp[i + len(word)] with the minimum cost
        
        Time Complexity: O(n * m * l) where n = len(target), m = len(words), 
                         l = average length of words
        Space Complexity: O(n) for the dp array
        """
        n = len(target)
        # dp[i] = minimum cost to build target[0:i]
        # Initialize with infinity, except dp[0] = 0 (empty string costs 0)
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        
        # For each position in the target string
        for i in range(n):
            # If we can't reach position i, skip
            if dp[i] == float('inf'):
                continue
            
            # Try each word to see if it matches at position i
            for word, cost in zip(words, costs):
                word_len = len(word)
                # Check if word fits and matches the target at position i
                if i + word_len <= n and target[i:i + word_len] == word:
                    # Update the cost to reach position i + word_len
                    dp[i + word_len] = min(dp[i + word_len], dp[i] + cost)
        
        # If we reached the end, return the cost; otherwise return -1
        return dp[n] if dp[n] != float('inf') else -1
