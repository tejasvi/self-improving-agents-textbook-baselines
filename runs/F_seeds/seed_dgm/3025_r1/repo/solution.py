from typing import List


class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1
        cnt = [0] * 64
        for x in nums:
            cnt[x.bit_length() - 1] += 1
        ops = 0
        for i in range(32):
            if (target >> i) & 1:
                if cnt[i] == 0:
                    j = i + 1
                    while j < 64 and cnt[j] == 0:
                        j += 1
                    if j >= 64:
                        return -1
                    # split one 2^j into 2^i pieces: one at each level i+1..j-1, two at level i
                    ops += j - i
                    cnt[j] -= 1
                    for k in range(i + 1, j):
                        cnt[k] += 1
                    cnt[i] += 2
                cnt[i] -= 1
            # leftover pieces at level i can combine into level i+1
            cnt[i + 1] += cnt[i] // 2
            cnt[i] %= 2
        return ops
