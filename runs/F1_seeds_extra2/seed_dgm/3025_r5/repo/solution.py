from typing import List


class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1
        cnt = [0] * 64
        for x in nums:
            cnt[x.bit_length() - 1] += 1
        ans = 0
        for i in range(63):
            if (target >> i) & 1:
                if cnt[i] > 0:
                    cnt[i] -= 1
                else:
                    j = i + 1
                    while cnt[j] == 0:
                        j += 1
                    ans += j - i
                    cnt[j] -= 1
                    for k in range(i + 1, j):
                        cnt[k] += 1
            # leftover smaller powers can merge into larger ones for free
            cnt[i + 1] += cnt[i] // 2
        return ans
