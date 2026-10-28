from bisect import bisect_right
from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        a = sorted(nums)
        n = len(a)
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})

        def count(d: int) -> int:
            # p[i]: number of indices j with a[i] - a[j] >= d (they form prefix 0..p[i]-1)
            p = [bisect_right(a, a[i] - d) for i in range(n)]
            # dp[c][i]: number of valid subsequences of length c ending at index i
            dp = [[0] * n for _ in range(k + 1)]
            # prefix[c][m]: sum of dp[c][0..m-1]
            prefix = [[0] * (n + 1) for _ in range(k + 1)]
            for i in range(n):
                dp[1][i] = 1
            for c in range(1, k + 1):
                if c > 1:
                    for i in range(n):
                        dp[c][i] = prefix[c - 1][p[i]]
                pc = prefix[c]
                for i in range(n):
                    pc[i + 1] = pc[i] + dp[c][i]
            return prefix[k][n]

        ans = 0
        prev = 0
        for d in diffs:
            ans += (d - prev) * count(d)
            prev = d
        return ans % MOD
