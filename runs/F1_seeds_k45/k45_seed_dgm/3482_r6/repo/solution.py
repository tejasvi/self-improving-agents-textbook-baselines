class Solution:
    def minimumCost(self, target: str, words: List[str], costs: List[int]) -> int:
        """
        Find the minimum cost to construct the target string using words from the given array.
        
        Approach: Dynamic Programming
        - dp[i] = minimum cost to construct the first i characters of target
        - For each position i, try all words that can be appended at position i
        - If a word matches the substring starting at position i, update dp[i + len(word)]
        
        Time Complexity: O(n * m * w) where n is target length, m is words count, w is max word length
        Space Complexity: O(n) for the DP array
        """
        n = len(target)
        
        # dp[i] represents the minimum cost to construct target[0:i]
        # Initialize with infinity (impossible state)
        dp = [float('inf')] * (n + 1)
        dp[0] = 0  # Cost of empty string is 0
        
        # For each position in the target string
        for i in range(n):
            # If current position is unreachable, skip
            if dp[i] == float('inf'):
                continue
            
            # Try appending each word
            for word, cost in zip(words, costs):
                word_len = len(word)
                # Check if word can be appended at position i
                if i + word_len <= n and target[i:i + word_len] == word:
                    # Update the cost to reach position i + word_len
                    dp[i + word_len] = min(dp[i + word_len], dp[i] + cost)
        
        # If dp[n] is still infinity, it's impossible to construct target
        return dp[n] if dp[n] != float('inf') else -1
