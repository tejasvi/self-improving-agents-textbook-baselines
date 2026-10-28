from typing import *


class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1
        cnt = [0] * 64
        for x in nums:
            cnt[x.bit_length() - 1] += 1
        ans = 0
        for i in range(32):
            if (target >> i) & 1:
                if cnt[i] == 0:
                    j = i + 1
                    while j < 64 and cnt[j] == 0:
                        j += 1
                    if j >= 64:
                        return -1
                    ans += j - i
                    cnt[j] -= 1
                    for k in range(i, j):
                        cnt[k] += 1
                cnt[i] -= 1
            cnt[i + 1] += cnt[i] // 2
        return ans
