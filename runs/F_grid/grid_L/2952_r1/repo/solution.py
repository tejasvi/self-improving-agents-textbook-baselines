from typing import List


class Solution:
    def minimumTime(self, nums1: List[int], nums2: List[int], x: int) -> int:
        n = len(nums1)
        s1 = sum(nums1)
        s2 = sum(nums2)
        if s1 <= x:
            return 0
        # Items sorted by nums2 ascending; the j-th chosen item is zeroed at time j.
        items = sorted(zip(nums2, nums1))
        NEG = float("-inf")
        dp = [NEG] * (n + 1)
        dp[0] = 0
        for cnt, (b, a) in enumerate(items, 1):
            for j in range(cnt, 0, -1):
                if dp[j - 1] != NEG:
                    val = dp[j - 1] + a + j * b
                    if val > dp[j]:
                        dp[j] = val
        best = NEG
        for t in range(1, n + 1):
            best = max(best, dp[t])
            if best != NEG and s1 + t * s2 - best <= x:
                return t
        return -1
