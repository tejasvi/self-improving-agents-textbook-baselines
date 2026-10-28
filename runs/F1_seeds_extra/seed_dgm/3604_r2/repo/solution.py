class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        # S[i][k]: ways to partition i performers into k non-empty groups
        S = [[0] * (n + 1) for _ in range(n + 1)]
        S[0][0] = 1
        for i in range(1, n + 1):
            for k in range(1, i + 1):
                S[i][k] = (k * S[i - 1][k] + S[i - 1][k - 1]) % MOD
        ans = 0
        perm = 1  # x * (x-1) * ... * (x-k+1)
        ypow = 1
        for k in range(1, min(n, x) + 1):
            perm = perm * (x - k + 1) % MOD
            ypow = ypow * y % MOD
            ans = (ans + S[n][k] * perm % MOD * ypow) % MOD
        return ans
