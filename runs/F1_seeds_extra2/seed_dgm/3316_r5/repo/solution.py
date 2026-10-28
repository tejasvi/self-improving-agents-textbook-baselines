from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        s = sorted(nums)
        n = len(s)

        # Distinct positive pairwise differences (candidate minimum values).
        diffs = sorted({s[j] - s[i] for i in range(n) for j in range(i + 1, n) if s[j] - s[i] > 0})

        def count(d: int) -> int:
            # lo[i] = largest p < i with s[i] - s[p] >= d, or -1 if none.
            # Since s is sorted, valid predecessors of i form the prefix [0, lo[i]].
            lo = [-1] * n
            for i in range(n):
                p = i - 1
                while p >= 0 and s[i] - s[p] < d:
                    p -= 1
                lo[i] = p
            # dp[i] = number of valid subsequences of current length ending at i.
            dp = [1] * n
            for _ in range(k - 1):
                # prefix sums of dp
                pre = [0] * (n + 1)
                for i in range(n):
                    pre[i + 1] = pre[i] + dp[i]
                dp = [pre[lo[i] + 1] % MOD for i in range(n)]
            return sum(dp) % MOD

        total = 0
        prev = 0
        for D in diffs:
            total = (total + (D - prev) * count(D)) % MOD
            prev = D
        return total % MOD
