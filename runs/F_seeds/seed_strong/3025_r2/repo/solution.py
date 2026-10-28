from typing import *


class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1
        B = 32
        cnt = [0] * (B + 1)
        for x in nums:
            cnt[x.bit_length() - 1] += 1
        ans = 0
        for i in range(B):
            if (target >> i) & 1:
                if cnt[i] == 0:
                    j = i + 1
                    while j < B and cnt[j] == 0:
                        j += 1
                    if j == B:
                        return -1
                    ans += j - i
                    cnt[j] -= 1
                    # 2^j = 2^i + 2^i + 2^{i+1} + ... + 2^{j-1}
                    for k in range(i, j):
                        cnt[k] += 1
                    # the extra 2^i is covered by the carry below
                    cnt[i] += 1
                cnt[i] -= 1
            cnt[i + 1] += cnt[i] // 2
        return ans
