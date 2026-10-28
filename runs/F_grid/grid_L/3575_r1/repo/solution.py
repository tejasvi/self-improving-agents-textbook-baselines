from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def k_or_sets(seq):
            # res[m] = set of OR values achievable by choosing exactly k
            # elements from seq[:m]; res[m] is empty if impossible.
            dp = [set() for _ in range(k + 1)]
            dp[0].add(0)
            res = [set() for _ in range(len(seq) + 1)]
            for i, x in enumerate(seq):
                for c in range(min(k, i + 1), 0, -1):
                    if dp[c - 1]:
                        dp[c].update(v | x for v in dp[c - 1])
                res[i + 1] = set(dp[k])
            return res

        pre = k_or_sets(nums)
        suf_rev = k_or_sets(nums[::-1])  # suf_rev[t] covers nums[n-t:]
        best = 0
        for m in range(k, n - k + 1):
            left = pre[m]
            right = suf_rev[n - m]
            if not left or not right:
                continue
            for a in left:
                for b in right:
                    if a ^ b > best:
                        best = a ^ b
        return best
