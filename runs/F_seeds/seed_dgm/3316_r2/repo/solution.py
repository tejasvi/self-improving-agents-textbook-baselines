from typing import List
from bisect import bisect_right


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10**9 + 7
        a = sorted(nums)
        n = len(a)
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})
        total = 0
        prev = 0
        for d in diffs:
            w = d - prev
            prev = d
            if d == 0:
                continue
            # p[i] = number of indices j with a[j] <= a[i] - d (all valid predecessors are j < p[i])
            p = [bisect_right(a, a[i] - d) for i in range(n)]
            # dp[i][c]: number of valid subsequences of length c ending at index i
            # pre[i][c] = sum_{j<i} dp[j][c]
            dp = [[0] * (k + 1) for _ in range(n)]
            pre = [[0] * (k + 1) for _ in range(n + 1)]
            for i in range(n):
                dp[i][1] = 1
                pi = p[i]
                for c in range(2, k + 1):
                    dp[i][c] = pre[pi][c - 1]
                for c in range(1, k + 1):
                    pre[i + 1][c] = (pre[i][c] + dp[i][c]) % MOD
            cnt = pre[n][k]
            total = (total + w % MOD * cnt) % MOD
        return total % MOD
