from typing import List


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
                    # Split the smallest available larger power 2^j down to 2^i.
                    j = i + 1
                    while j < 63 and cnt[j] == 0:
                        j += 1
                    if j >= 63:
                        return -1
                    # 2^j -> 2^i + 2^i + 2^(i+1) + ... + 2^(j-1), costs j - i ops.
                    cnt[j] -= 1
                    for k in range(i, j):
                        cnt[k] += 1
                    cnt[i] -= 1  # one copy of 2^i is used for the target bit
                    ops += j - i
            # Leftover smaller powers can be combined for free (as a subsequence).
            if i + 1 < 64:
                cnt[i + 1] += cnt[i] // 2
        return ops
