class Solution:
    def numberOfWays(self, n: int, x: int, y: int) -> int:
        MOD = 10**9 + 7
        # Stirling numbers of the second kind, row n: S(n, k)
        # S(i, k) = k * S(i-1, k) + S(i-1, k-1)
        prev = [1] + [0] * n  # row i=0
        for i in range(1, n + 1):
            cur = [0] * (n + 1)
            for k in range(1, i + 1):
                cur[k] = (k * prev[k] + prev[k - 1]) % MOD
            prev = cur
        stirling = prev

        ans = 0
        perm = 1  # P(x, k) = x*(x-1)*...*(x-k+1)
        power = 1  # y^k
        for k in range(1, min(n, x) + 1):
            perm = perm * (x - k + 1) % MOD
            power = power * y % MOD
            ans = (ans + stirling[k] * perm % MOD * power) % MOD
        return ans
