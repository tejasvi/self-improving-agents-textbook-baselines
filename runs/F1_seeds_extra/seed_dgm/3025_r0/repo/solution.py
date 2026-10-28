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
                    # Split the smallest available larger power down to 2^i.
                    j = i + 1
                    while j < 63 and cnt[j] == 0:
                        j += 1
                    if j >= 63:
                        return -1
                    cnt[j] -= 1
                    for k in range(i, j):
                        cnt[k] += 1
                    ans += j - i
            # Leftover units of 2^i pair up into 2^(i+1) for free.
            cnt[i + 1] += cnt[i] // 2
            cnt[i] %= 2
        return ans
