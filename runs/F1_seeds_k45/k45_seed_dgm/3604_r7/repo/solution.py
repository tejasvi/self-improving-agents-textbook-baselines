class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        
        # Compute Stirling numbers of the second kind S(n, k)
        # S(n, k) = number of ways to partition n items into k non-empty subsets
        # Using dynamic programming: S(n, k) = k * S(n-1, k) + S(n-1, k-1)
        S = [[0] * (n + 1) for _ in range(n + 1)]
        S[0][0] = 1
        
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                S[i][j] = (j * S[i - 1][j] + S[i - 1][j - 1]) % MOD
        
        # Helper function to compute modular exponentiation
        def mod_pow(base, exp, mod):
            result = 1
            base %= mod
            while exp > 0:
                if exp % 2 == 1:
                    result = (result * base) % mod
                exp //= 2
                base = (base * base) % mod
            return result
        
        # Helper function to compute permutation P(x, k) = x * (x-1) * ... * (x-k+1)
        def permutation(x, k):
            if k > x:
                return 0
            result = 1
            for i in range(x, x - k, -1):
                result = (result * i) % MOD
            return result
        
        # Sum over all possible number of non-empty bands k
        total = 0
        for k in range(1, min(n, x) + 1):
            # Number of ways to partition n performers into k groups
            stirling = S[n][k]
            # Number of ways to assign k groups to x stages (ordered assignment)
            perm = permutation(x, k)
            # Number of ways to score k bands with scores from 1 to y
            scores = mod_pow(y, k, MOD)
            
            # Add to total
            ways = (stirling * perm) % MOD
            ways = (ways * scores) % MOD
            total = (total + ways) % MOD
        
        return total
