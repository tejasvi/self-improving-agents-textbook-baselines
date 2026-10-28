from typing import List


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        def square_free_part(x: int) -> int:
            # Remove every square factor so that x = s * k^2 with s square-free.
            result = 1
            p = 2
            while p * p <= x:
                exp = 0
                while x % p == 0:
                    x //= p
                    exp += 1
                if exp % 2 == 1:
                    result *= p
                p += 1
            return result * x

        groups = {}
        for i, value in enumerate(nums, start=1):
            key = square_free_part(i)
            groups[key] = groups.get(key, 0) + value
        return max(groups.values())
