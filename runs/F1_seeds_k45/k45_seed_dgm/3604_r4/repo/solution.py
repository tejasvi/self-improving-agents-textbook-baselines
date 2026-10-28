class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        
        # Compute Stirling numbers of the second kind S(n, k)
        # S(n, k) = number of ways to partition n items into k non-empty subsets
        # We'll use dynamic programming: S(n, k) = k*S(n-1, k) + S(n-1, k-1)
        
        stirling = [[0] * (n + 1) for _ in range(n + 1)]
        stirling[0][0] = 1
        
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                stirling[i][j] = (j * stirling[i-1][j] + stirling[i-1][j-1]) % MOD
        
        # Precompute factorials
        fact = [1] * (x + 1)
        for i in range(1, x + 1):
            fact[i] = (fact[i-1] * i) % MOD
        
        # Precompute powers of y
        pow_y = [1] * (n + 1)
        for i in range(1, n + 1):
            pow_y[i] = (pow_y[i-1] * y) % MOD
        
        result = 0
        # Sum over all possible numbers of non-empty stages k
        # k ranges from 1 to min(n, x)
        for k in range(1, min(n, x) + 1):
            # Number of surjections from n performers to k stages
            # = k! * S(n, k)
            surjections = (fact[k] * stirling[n][k]) % MOD
            
            # Each of the k bands gets a score from 1 to y
            # = y^k ways
            scores = pow_y[k]
            
            # Total ways for this k
            ways = (surjections * scores) % MOD
            result = (result + ways) % MOD
        
        return result
