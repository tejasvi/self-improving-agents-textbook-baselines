from typing import List

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # Count occurrences of each power of two (up to 2^30)
        MAX_BIT = 31  # support values up to 2^30
        cnt = [0] * MAX_BIT
        for x in nums:
            bit = x.bit_length() - 1
            cnt[bit] += 1

        ops = 0
        for i in range(MAX_BIT):
            # If target requires this bit
            if (target >> i) & 1:
                if cnt[i] > 0:
                    cnt[i] -= 1
                else:
                    # Find a larger power to split
                    j = i + 1
                    while j < MAX_BIT and cnt[j] == 0:
                        j += 1
                    if j == MAX_BIT:
                        return -1  # impossible
                    # Split down from j to i, each split counts as one operation
                    while j > i:
                        cnt[j] -= 1
                        cnt[j - 1] += 2
                        ops += 1
                        j -= 1
                    cnt[i] -= 1  # use one of the newly created pieces
            # Carry over pairs to the next bit (if any)
            if i + 1 < MAX_BIT:
                cnt[i + 1] += cnt[i] // 2
                cnt[i] %= 2
        return ops
