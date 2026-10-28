class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials
        max_val = max(n, x) + 1
        fact = [1] * max_val
        for i in range(1, max_val):
            fact[i] = (fact[i-1] * i) % MOD
        
        def mod_inverse(a):
            """Calculate modular inverse using Fermat's little theorem"""
            return pow(a, MOD - 2, MOD)
        
        def comb(n, k):
            """Calculate C(n, k) mod MOD"""
            if k > n or k < 0:
                return 0
            if k == 0 or k == n:
                return 1
            
            numerator = fact[n]
            denominator = (fact[k] * fact[n - k]) % MOD
            return (numerator * mod_inverse(denominator)) % MOD
        
        def surjections(n, k):
            """Calculate number of surjections from n items to k labeled groups using inclusion-exclusion"""
            if k > n or k <= 0:
                return 0
            if k == 1:
                return 1
            
            result = 0
            # Inclusion-exclusion: sum (-1)^i * C(k, i) * (k-i)^n
            for i in range(k + 1):
                sign = 1 if i % 2 == 0 else -1
                term = (comb(k, i) * pow(k - i, n, MOD)) % MOD
                result = (result + sign * term) % MOD
            
            return result % MOD
        
        # Sum over all possible numbers of non-empty stages k
        total = 0
        for k in range(1, min(n, x) + 1):
            # C(x, k) ways to choose which k stages have performers
            # surjections(n, k) ways to assign n performers to k stages such that all are used
            # y^k ways to score the k bands
            ways = (comb(x, k) * surjections(n, k)) % MOD
            ways = (ways * pow(y, k, MOD)) % MOD
            total = (total + ways) % MOD
        
        return total
