class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        # S[k] = Stirling number of the second kind S(i, k), built row by row.
        S = [1] + [0] * n  # row i = 0
        for i in range(1, n + 1):
            new = [0] * (n + 1)
            for k in range(1, i + 1):
                new[k] = (k * S[k] + S[k - 1]) % MOD
            S = new
        ans = 0
        falling = 1  # x * (x-1) * ... * (x-k+1)
        ypow = 1
        for k in range(0, min(n, x) + 1):
            if k > 0:
                falling = falling * (x - k + 1) % MOD
                ypow = ypow * y % MOD
            ans = (ans + S[k] * falling % MOD * ypow) % MOD
        return ans
