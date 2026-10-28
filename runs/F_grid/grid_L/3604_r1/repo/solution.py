class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        m = min(n, x)
        # S[i][k]: Stirling numbers of the second kind (partitions of i items into k non-empty groups)
        prev = [1] + [0] * m  # i = 0
        for i in range(1, n + 1):
            cur = [0] * (m + 1)
            for k in range(1, min(i, m) + 1):
                cur[k] = (k * prev[k] + prev[k - 1]) % MOD
            prev = cur
        S = prev  # S[k] = S(n, k)
        ans = 0
        perm = 1  # P(x, k)
        ypow = 1  # y^k
        for k in range(0, m + 1):
            if k > 0:
                perm = perm * (x - k + 1) % MOD
                ypow = ypow * y % MOD
            ans = (ans + S[k] * perm % MOD * ypow) % MOD
        return ans
