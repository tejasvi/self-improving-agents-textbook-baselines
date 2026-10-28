from typing import List


class Solution:
    def maxSelectedElements(self, nums: List[int]) -> int:
        # f[v] = longest run of consecutive values ending at v, using
        # distinct elements processed so far (each element assigned to x or x+1).
        f = {}
        best = 0
        for x in sorted(nums):
            # Assign current element to x+1 first (reads old f[x]), then to x
            # (reads old f[x-1], which the current element can never modify).
            new_hi = f.get(x, 0) + 1
            if new_hi > f.get(x + 1, 0):
                f[x + 1] = new_hi
            new_lo = f.get(x - 1, 0) + 1
            if new_lo > f.get(x, 0):
                f[x] = new_lo
            best = max(best, f[x], f[x + 1])
        return best
