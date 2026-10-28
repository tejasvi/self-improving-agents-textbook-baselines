from typing import List


class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1

        B = 64
        cnt = [0] * B
        for x in nums:
            cnt[x.bit_length() - 1] += 1

        ans = 0
        for i in range(B - 1):
            if (target >> i) & 1:
                if cnt[i] > 0:
                    cnt[i] -= 1
                else:
                    j = i + 1
                    while j < B and cnt[j] == 0:
                        j += 1
                    if j == B:
                        return -1
                    # split 2^j down to 2^i: costs j - i operations
                    ans += j - i
                    cnt[j] -= 1
                    for k in range(i, j):
                        cnt[k] += 1
            # leftover smaller powers can combine into the next bit
            cnt[i + 1] += cnt[i] // 2
        return ans
