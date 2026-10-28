from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n) if a[j] - a[i] > 0})

        total = 0
        prev = 0
        for v in diffs:
            weight = v - prev
            prev = v
            # p[i] = largest index j with a[i] - a[j] >= v (or -1)
            p = [-1] * n
            for i in range(n):
                j = i - 1
                while j >= 0 and a[i] - a[j] < v:
                    j -= 1
                p[i] = j
            # dp[i][c]: number of ways to pick c elements ending at index i
            # prefix[i][c] = sum_{t<=i} dp[t][c]
            dp = [[0] * (k + 1) for _ in range(n)]
            pref = [[0] * (k + 1) for _ in range(n)]
            for i in range(n):
                dp[i][1] = 1
                if p[i] >= 0:
                    for c in range(2, k + 1):
                        dp[i][c] = pref[p[i]][c - 1]
                for c in range(1, k + 1):
                    pref[i][c] = ((pref[i - 1][c] if i > 0 else 0) + dp[i][c]) % MOD
            count = pref[n - 1][k] % MOD
            total = (total + weight % MOD * count) % MOD
        return total % MOD
