from typing import List


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        def square_free_part(x: int) -> int:
            result = 1
            p = 2
            while p * p <= x:
                if x % p == 0:
                    cnt = 0
                    while x % p == 0:
                        x //= p
                        cnt += 1
                    if cnt % 2 == 1:
                        result *= p
                p += 1
            return result * x

        groups = {}
        for i, v in enumerate(nums, start=1):
            key = square_free_part(i)
            groups[key] = groups.get(key, 0) + v
        return max(groups.values()) if groups else 0
