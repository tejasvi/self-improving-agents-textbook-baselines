from typing import *


class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1
        cnt = [0] * 64
        for x in nums:
            cnt[x.bit_length() - 1] += 1
        ops = 0
        for i in range(32):
            if not (target >> i) & 1:
                cnt[i + 1] += cnt[i] // 2
                continue
            if cnt[i] > 0:
                cnt[i] -= 1
            else:
                j = i + 1
                while j < 63 and cnt[j] == 0:
                    j += 1
                if j >= 63:
                    return -1
                # split 2^j down to 2^i, using one 2^i
                cnt[j] -= 1
                for k in range(i, j):
                    cnt[k] += 1
                ops += j - i
                cnt[i] -= 1
            cnt[i + 1] += cnt[i] // 2
        return ops
