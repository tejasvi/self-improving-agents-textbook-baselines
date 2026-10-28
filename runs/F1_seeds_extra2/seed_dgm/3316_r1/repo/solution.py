from typing import List


class Solution:
    def sumOfPowers(self, nums: List[int], k: int) -> int:
        MOD = 10 ** 9 + 7
        a = sorted(nums)
        n = len(a)
        diffs = sorted({a[j] - a[i] for i in range(n) for j in range(i + 1, n)})

        # For each j, p[j] = largest index i with a[i] <= a[j] - d (computed per d).
        def count(d: int) -> int:
            # dp[j][c]: number of length-c subsequences ending at j with all
            # consecutive gaps >= d.
            # Valid predecessors of j are indices 0..p[j] (since array is sorted).
            p = [-1] * n
            ptr = -1
            for j in range(n):
                while ptr + 1 < n and a[ptr + 1] <= a[j] - d:
                    ptr += 1
                p[j] = ptr
            # prefix[j][c] = sum_{i<=j} dp[i][c]
            prefix = [[0] * (k + 1) for _ in range(n)]
            dp_last = [0] * (k + 1)
            for j in range(n):
                dp = [0] * (k + 1)
                dp[1] = 1
                if p[j] >= 0:
                    pre = prefix[p[j]]
                    for c in range(2, k + 1):
                        dp[c] = pre[c - 1]
                row = prefix[j]
                for c in range(1, k + 1):
                    row[c] = (prefix[j - 1][c] if j > 0 else 0) + dp[c]
                dp_last = dp
            # total over all ending positions for length k
            return sum(prefix[j][k] - (prefix[j - 1][k] if j > 0 else 0) for j in range(n)) % MOD

        total = 0
        prev = 0
        for v in diffs:
            if v == 0:
                prev = 0
                continue
            total += (v - prev) * count(v)
            prev = v
        return total % MOD
