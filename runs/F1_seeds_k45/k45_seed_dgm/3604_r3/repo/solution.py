class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        
        # Compute Stirling numbers of the second kind S(n, k)
        # S(n, k) = number of ways to partition n elements into k non-empty subsets
        stirling = [[0] * (n + 1) for _ in range(n + 1)]
        stirling[0][0] = 1
        
        for i in range(1, n + 1):
            for j in range(1, i + 1):
                stirling[i][j] = (j * stirling[i-1][j] + stirling[i-1][j-1]) % MOD
        
        # Compute factorials and inverse factorials for combinations
        fact = [1] * (x + 1)
        for i in range(1, x + 1):
            fact[i] = (fact[i-1] * i) % MOD
        
        # Helper function to compute modular inverse
        def modinv(a, m=MOD):
            return pow(a, m - 2, m)
        
        # Helper function to compute C(n, k)
        def comb(n, k):
            if k > n or k < 0:
                return 0
            return (fact[n] * modinv(fact[k]) % MOD) * modinv(fact[n - k]) % MOD
        
        result = 0
        # For each possible number of non-empty stages k
        for k in range(1, min(n, x) + 1):
            # S(n, k): partition n performers into k groups
            # C(x, k): choose which k stages to use
            # k!: assign k groups to k stages (already in fact[k])
            # y^k: assign scores to k bands
            ways = stirling[n][k] * comb(x, k) % MOD
            ways = ways * fact[k] % MOD
            ways = ways * pow(y, k, MOD) % MOD
            result = (result + ways) % MOD
        
        return result
