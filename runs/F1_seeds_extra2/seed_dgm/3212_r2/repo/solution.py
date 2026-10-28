from typing import List


class Solution:
    def numberOfGoodPartitions(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        last = {}
        for i, x in enumerate(nums):
            last[x] = i
        # Count blocks: a cut after index i is allowed only if no value
        # spans across it, i.e., max last occurrence of prefix <= i.
        blocks = 0
        reach = -1
        for i, x in enumerate(nums):
            if i > reach:
                blocks += 1
            reach = max(reach, last[x])
        return pow(2, blocks - 1, MOD)
