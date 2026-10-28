from typing import List


class Solution:
    def minimumTime(self, nums1: List[int], nums2: List[int], x: int) -> int:
        n = len(nums1)
        s1 = sum(nums1)
        s2 = sum(nums2)
        # Sort by nums2 ascending: items zeroed later should have larger growth.
        items = sorted(zip(nums2, nums1))
        NEG = float("-inf")
        # dp[j] = max total reduction when exactly j items are zeroed,
        # the j-th chosen item (in sorted order) being zeroed at second j.
        dp = [NEG] * (n + 1)
        dp[0] = 0
        for i, (b, a) in enumerate(items):
            for j in range(i + 1, 0, -1):
                if dp[j - 1] != NEG:
                    val = dp[j - 1] + a + j * b
                    if val > dp[j]:
                        dp[j] = val
        for t in range(n + 1):
            if s1 + t * s2 - dp[t] <= x:
                return t
        return -1
