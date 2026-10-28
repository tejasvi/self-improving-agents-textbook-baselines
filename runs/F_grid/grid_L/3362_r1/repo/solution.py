from typing import List


class Solution:
    def medianOfUniquenessArray(self, nums: List[int]) -> int:
        n = len(nums)
        total = n * (n + 1) // 2
        need = (total + 1) // 2  # index (total-1)//2 in 0-based => count of values <= ans must be >= need

        def count_at_most(k: int) -> int:
            # number of subarrays with at most k distinct elements
            freq = {}
            left = 0
            distinct = 0
            res = 0
            for right, x in enumerate(nums):
                f = freq.get(x, 0)
                if f == 0:
                    distinct += 1
                freq[x] = f + 1
                while distinct > k:
                    y = nums[left]
                    freq[y] -= 1
                    if freq[y] == 0:
                        distinct -= 1
                    left += 1
                res += right - left + 1
            return res

        lo, hi = 1, max(1, len(set(nums)))
        while lo < hi:
            mid = (lo + hi) // 2
            if count_at_most(mid) >= need:
                hi = mid
            else:
                lo = mid + 1
        return lo
