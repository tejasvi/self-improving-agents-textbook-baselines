class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        m = min(n, x)
        # Stirling numbers of the second kind S(n, k), rolling over i
        S = [1] + [0] * m  # S(0, 0) = 1
        for i in range(1, n + 1):
            new = [0] * (m + 1)
            for k in range(1, min(i, m) + 1):
                new[k] = (k * S[k] + S[k - 1]) % MOD
            S = new
        ans = 0
        falling = 1  # P(x, k)
        ypow = 1     # y^k
        for k in range(0, m + 1):
            if k > 0:
                falling = falling * (x - k + 1) % MOD
                ypow = ypow * y % MOD
            ans = (ans + S[k] * falling % MOD * ypow) % MOD
        return ans
