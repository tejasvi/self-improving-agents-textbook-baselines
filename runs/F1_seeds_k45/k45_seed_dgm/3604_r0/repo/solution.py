class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        
        # Compute Stirling numbers of the second kind
        # S(n, k) = number of ways to partition n items into k non-empty subsets
        # Using dynamic programming: S(n, k) = k*S(n-1, k) + S(n-1, k-1)
        S = [[0] * (n + 1) for _ in range(n + 1)]
        S[0][0] = 1
        
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                S[i][j] = (j * S[i-1][j] + S[i-1][j-1]) % MOD
        
        result = 0
        
        # For each possible number of non-empty stages from 1 to min(n, x)
        for k in range(1, min(n, x) + 1):
            # S(n, k) = number of ways to partition n performers into k groups
            stirling = S[n][k]
            
            # P(x, k) = x * (x-1) * ... * (x-k+1)
            # Number of ways to assign k groups to k stages out of x stages
            perm = 1
            for i in range(k):
                perm = (perm * (x - i)) % MOD
            
            # y^k = number of ways to assign scores to k bands
            score_ways = pow(y, k, MOD)
            
            # Contribution of k non-empty stages
            contribution = (stirling * perm % MOD) * score_ways % MOD
            result = (result + contribution) % MOD
        
        return result
