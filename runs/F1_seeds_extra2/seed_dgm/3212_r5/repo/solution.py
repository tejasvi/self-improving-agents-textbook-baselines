from typing import List


class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        n = len(nums)
        last = {}
        for i, x in enumerate(nums):
            last[x] = i
        # Count the number of positions i (cut after i) where no value's
        # span [first, last] crosses the boundary between i and i+1.
        cuts = 0
        reach = -1
        for i, x in enumerate(nums):
            if last[x] > reach:
                reach = last[x]
            if reach == i:
                cuts += 1
        return pow(2, cuts - 1, MOD)
