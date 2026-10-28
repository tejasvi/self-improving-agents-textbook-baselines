from typing import List


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        n = len(nums)

        def square_free_part(x: int) -> int:
            result = 1
            p = 2
            while p * p <= x:
                count = 0
                while x % p == 0:
                    x //= p
                    count += 1
                if count % 2 == 1:
                    result *= p
                p += 1
            if x > 1:
                result *= x
            return result

        sums = {}
        for i in range(1, n + 1):
            key = square_free_part(i)
            sums[key] = sums.get(key, 0) + nums[i - 1]
        return max(sums.values()) if sums else 0
