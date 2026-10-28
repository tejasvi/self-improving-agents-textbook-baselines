from typing import List


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        # Indices i and j (1-indexed) form a complete pair iff i*j is a perfect
        # square, i.e. they share the same square-free part. Group by that key.
        n = len(nums)
        groups = {}
        for i in range(1, n + 1):
            key = i
            d = 2
            while d * d <= key:
                sq = d * d
                while key % sq == 0:
                    key //= sq
                d += 1
            groups[key] = groups.get(key, 0) + nums[i - 1]
        return max(groups.values()) if groups else 0
