from typing import *


class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1
        cnt = [0] * 65
        for x in nums:
            cnt[x.bit_length() - 1] += 1
        ops = 0
        for i in range(64):
            if (target >> i) & 1:
                if cnt[i] > 0:
                    cnt[i] -= 1
                else:
                    j = i + 1
                    while j < 64 and cnt[j] == 0:
                        j += 1
                    if j >= 64:
                        return -1
                    ops += j - i
                    cnt[j] -= 1
                    for k in range(i, j):
                        cnt[k] += 1
            # leftover small items can be merged (free) into the next level
            cnt[i + 1] += cnt[i] // 2
        return ops
