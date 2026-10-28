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
            if target >> i & 1:
                if cnt[i] == 0:
                    # Split the smallest larger power 2^j down to 2^i.
                    j = i
                    while cnt[j] == 0:
                        j += 1
                    ans += j - i
                    cnt[j] -= 1
                    # 2^j = 2^i + 2^i + 2^(i+1) + ... + 2^(j-1)
                    for k in range(i, j):
                        cnt[k] += 1
                    cnt[i] += 1
                cnt[i] -= 1
            # Pair up leftover 2^i into 2^(i+1); free to combine.
            cnt[i + 1] += cnt[i] // 2
        return ans
