class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        m = min(n, x)
        # Stirling numbers of the second kind S(n, k), rolling over i
        prev = [1] + [0] * m  # S(0, k)
        for i in range(1, n + 1):
            cur = [0] * (m + 1)
            for k in range(1, min(i, m) + 1):
                cur[k] = (k * prev[k] + prev[k - 1]) % MOD
            prev = cur
        stirling = prev  # S(n, k)
        ans = 0
        perm = 1  # P(x, k)
        power = 1  # y^k
        for k in range(1, m + 1):
            perm = perm * (x - k + 1) % MOD
            power = power * y % MOD
            ans = (ans + stirling[k] * perm % MOD * power) % MOD
        return ans
