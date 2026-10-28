from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def prefix_sets(seq):
            # out[m] = set of OR values achievable by choosing exactly k
            # elements from seq[:m] (empty set if impossible).
            dp = [set() for _ in range(k + 1)]
            dp[0].add(0)
            out = [None] * (n + 1)
            out[0] = set(dp[k])
            for i, x in enumerate(seq):
                for j in range(min(k, i + 1), 0, -1):
                    if dp[j - 1]:
                        dp[j].update(o | x for o in dp[j - 1])
                out[i + 1] = set(dp[k])
            return out

        pre = prefix_sets(nums)
        suf = prefix_sets(nums[::-1])  # suf[t] covers the last t elements

        best = 0
        for m in range(k, n - k + 1):
            L = pre[m]
            R = suf[n - m]
            for a in L:
                for b in R:
                    v = a ^ b
                    if v > best:
                        best = v
        return best
