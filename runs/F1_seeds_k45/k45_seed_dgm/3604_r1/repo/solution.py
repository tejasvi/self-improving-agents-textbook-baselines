class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        
        # Compute Stirling numbers of the second kind S(n, k)
        # S(n, k) is the number of ways to partition n items into k non-empty subsets
        # We'll use dynamic programming: S(n, k) = k * S(n-1, k) + S(n-1, k-1)
        
        # Create a table for Stirling numbers
        stirling = [[0] * (n + 1) for _ in range(n + 1)]
        
        # Base cases
        for i in range(n + 1):
            stirling[i][0] = 0
        stirling[0][0] = 1
        
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                stirling[i][j] = (j * stirling[i-1][j] + stirling[i-1][j-1]) % MOD
        
        # Compute the answer
        result = 0
        
        # For each possible number of non-empty stages k
        for k in range(1, min(n, x) + 1):
            # Number of ways to choose k stages from x stages and assign groups to them
            # This is P(x, k) = x * (x-1) * ... * (x-k+1)
            permutations = 1
            for i in range(k):
                permutations = (permutations * (x - i)) % MOD
            
            # Number of ways to partition n performers into k non-empty groups
            partitions = stirling[n][k]
            
            # Number of ways to assign scores to k bands
            scores = pow(y, k, MOD)
            
            # Add to result
            ways = (permutations * partitions % MOD) * scores % MOD
            result = (result + ways) % MOD
        
        return result
