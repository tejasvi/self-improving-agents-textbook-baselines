class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        # We need to count assignments of n performers to x stages (each performer chooses a stage) and then assign a score in [1, y] to each non-empty stage (band).
        # The total ways = sum_{k=1..min(n,x)} (number of ways to have exactly k non-empty stages) * y^k.
        # Number of ways to assign n performers to exactly k non-empty stages (out of x) is: choose which k stages are used: C(x, k), then onto functions from n performers to those k stages: k! * S(n, k) where S(n,k) is Stirling numbers of second kind.
        # So total = sum_{k=1}^{min(n,x)} C(x, k) * k! * S(n, k) * y^k.
        # Simplify C(x,k)*k! = P(x,k) (falling factorial) = x*(x-1)*...*(x-k+1).
        # Compute Stirling numbers S(n,k) via DP O(n*x).
        max_k = min(n, x)
        # Precompute Stirling numbers of second kind up to n,k.
        S = [[0] * (max_k + 1) for _ in range(n + 1)]
        S[0][0] = 1
        for i in range(1, n + 1):
            for k in range(1, min(i, max_k) + 1):
                S[i][k] = (S[i-1][k-1] + k * S[i-1][k]) % MOD
        # Precompute falling factorial P(x,k).
        falling = [1] * (max_k + 1)
        for k in range(1, max_k + 1):
            falling[k] = falling[k-1] * (x - k + 1) % MOD
        # Precompute powers of y.
        pow_y = [1] * (max_k + 1)
        for k in range(1, max_k + 1):
            pow_y[k] = pow_y[k-1] * y % MOD
        ans = 0
        for k in range(1, max_k + 1):
            ans = (ans + falling[k] * S[n][k] % MOD * pow_y[k]) % MOD
        return ans
