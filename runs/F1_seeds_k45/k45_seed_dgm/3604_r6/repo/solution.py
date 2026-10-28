class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        
        # Compute Stirling numbers of the second kind S(n, k)
        # S(n, k) = number of ways to partition n objects into k non-empty subsets
        S = [[0] * (n + 1) for _ in range(n + 1)]
        S[0][0] = 1
        
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                S[i][j] = (j * S[i-1][j] + S[i-1][j-1]) % MOD
        
        # Precompute factorials
        fact = [1] * (x + 1)
        for i in range(1, x + 1):
            fact[i] = (fact[i-1] * i) % MOD
        
        # Precompute powers of y
        y_pow = [1] * (x + 1)
        for i in range(1, x + 1):
            y_pow[i] = (y_pow[i-1] * y) % MOD
        
        result = 0
        
        # Sum over all possible numbers of non-empty stages k
        for k in range(1, min(n, x) + 1):
            # C(x, k) = x! / (k! * (x-k)!)
            # We can compute it as x * (x-1) * ... * (x-k+1) / k!
            comb = 1
            for i in range(k):
                comb = (comb * (x - i)) % MOD
            comb = (comb * pow(fact[k], MOD - 2, MOD)) % MOD  # Divide by k!
            
            # Number of surjections from n to k stages
            surjections = (fact[k] * S[n][k]) % MOD
            
            # Total ways for this k
            ways = (comb * surjections) % MOD
            ways = (ways * y_pow[k]) % MOD
            
            result = (result + ways) % MOD
        
        return result
