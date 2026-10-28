class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        
        # Compute Stirling numbers of the second kind S(n, k)
        # S(n, k) = number of ways to partition n items into k non-empty groups
        stirling = [[0] * (n + 1) for _ in range(n + 1)]
        stirling[0][0] = 1
        
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                stirling[i][j] = (j * stirling[i - 1][j] + stirling[i - 1][j - 1]) % MOD
        
        # Compute factorials for permutations P(x, k) = x!/(x-k)!
        fact = [1] * (x + 1)
        for i in range(1, x + 1):
            fact[i] = (fact[i - 1] * i) % MOD
        
        result = 0
        
        # Sum over all possible numbers of non-empty stages k
        for k in range(1, min(n, x) + 1):
            # S(n, k) = ways to partition n performers into k non-empty groups
            s_n_k = stirling[n][k]
            
            # P(x, k) = ways to assign k groups to x stages
            # P(x, k) = x * (x-1) * ... * (x-k+1) = x! / (x-k)!
            p_x_k = 1
            for i in range(x, x - k, -1):
                p_x_k = (p_x_k * i) % MOD
            
            # y^k = ways to assign scores to k bands
            y_power_k = pow(y, k, MOD)
            
            # Add contribution for this k
            contribution = (s_n_k * p_x_k) % MOD
            contribution = (contribution * y_power_k) % MOD
            result = (result + contribution) % MOD
        
        return result
