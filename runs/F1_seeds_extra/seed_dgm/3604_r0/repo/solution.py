class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        # Stirling numbers of the second kind S[i][k]
        S = [[0] * (n + 1) for _ in range(n + 1)]
        S[0][0] = 1
        for i in range(1, n + 1):
            for k in range(1, i + 1):
                S[i][k] = (S[i - 1][k - 1] + k * S[i - 1][k]) % MOD
        ans = 0
        perm = 1  # x! / (x-k)!
        ypow = 1
        for k in range(1, min(n, x) + 1):
            perm = perm * (x - k + 1) % MOD
            ypow = ypow * y % MOD
            ans = (ans + S[n][k] * perm % MOD * ypow) % MOD
        return ans
