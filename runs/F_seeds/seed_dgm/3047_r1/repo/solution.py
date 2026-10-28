from typing import List


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        def square_free_part(x: int) -> int:
            # Remove every square factor from x.
            result = 1
            d = 2
            while d * d <= x:
                while x % (d * d) == 0:
                    x //= d * d
                if x % d == 0:
                    result *= d
                    x //= d
                d += 1
            return result * x

        # Indices i, j (1-indexed) form a complete pair iff i*j is a perfect
        # square, i.e. iff they share the same square-free part.
        groups = {}
        for i in range(1, len(nums) + 1):
            key = square_free_part(i)
            groups[key] = groups.get(key, 0) + nums[i - 1]
        return max(groups.values()) if groups else 0
