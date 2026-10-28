from typing import List


class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        B = 64
        cnt = [0] * (B + 1)
        for x in nums:
            cnt[x.bit_length() - 1] += 1

        ops = 0
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
                    # split one 2^j down to 2^i; leftovers: 2^k for k in [i, j-1]
                    ops += j - i
                    cnt[j] -= 1
                    for k in range(i, j):
                        cnt[k] += 1
            # unused smaller powers can be combined freely into the next bit
            cnt[i + 1] += cnt[i] // 2
        return ops
