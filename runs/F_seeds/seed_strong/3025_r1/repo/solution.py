from typing import *


class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1
        cnt = [0] * 64
        for x in nums:
            cnt[x.bit_length() - 1] += 1
        ops = 0
        for i in range(63):
            if (target >> i) & 1:
                if cnt[i] > 0:
                    cnt[i] -= 1
                else:
                    j = i + 1
                    while j < 63 and cnt[j] == 0:
                        j += 1
                    if j >= 63:
                        return -1
                    # split one 2^j down to 2^i: j-i operations,
                    # leaving one spare copy of each 2^k for i<=k<j (one 2^i consumed)
                    ops += j - i
                    cnt[j] -= 1
                    for k in range(i, j):
                        cnt[k] += 1
                    cnt[i] -= 1
            # unused smaller powers can be paired up for free into the next level
            cnt[i + 1] += cnt[i] // 2
        return ops
