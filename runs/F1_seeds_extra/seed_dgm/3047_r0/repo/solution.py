from typing import List


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        n = len(nums)

        def square_free_part(x: int) -> int:
            res = 1
            p = 2
            while p * p <= x:
                while x % (p * p) == 0:
                    x //= p * p
                if x % p == 0:
                    res *= p
                    x //= p
                p += 1
            return res * x

        groups = {}
        for i in range(1, n + 1):
            key = square_free_part(i)
            groups[key] = groups.get(key, 0) + nums[i - 1]
        return max(groups.values()) if groups else 0
