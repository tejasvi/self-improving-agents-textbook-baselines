from typing import List


class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1

        B = 64
        cnt = [0] * (B + 1)
        for x in nums:
            cnt[x.bit_length() - 1] += 1

        ans = 0
        for i in range(B):
            if (target >> i) & 1:
                if cnt[i] > 0:
                    cnt[i] -= 1
                else:
                    j = i + 1
                    while j < B and cnt[j] == 0:
                        j += 1
                    if j >= B:
                        return -1
                    # split one 2^j down to 2^i: j - i operations
                    ans += j - i
                    cnt[j] -= 1
                    for k in range(i + 1, j):
                        cnt[k] += 1
                    cnt[i] += 1  # the second copy of 2^i left over after using one
            # leftover smaller coins can be merged in pairs into the next level
            cnt[i + 1] += cnt[i] // 2
        return ans
