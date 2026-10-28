from typing import List

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # Count occurrences of each power of two
        MAX_BIT = 31  # enough for values up to 2^30 and target up to <2^31
        cnt = [0] * MAX_BIT
        for v in nums:
            # v is guaranteed to be a power of two
            bit = v.bit_length() - 1  # position of the set bit
            cnt[bit] += 1

        ops = 0
        # Process bits from low to high
        for i in range(MAX_BIT):
            # If current bit is needed in target
            if (target >> i) & 1:
                # If we have an element of this size, use it
                if cnt[i] > 0:
                    cnt[i] -= 1
                else:
                    # Find the next larger power that we can split
                    j = i + 1
                    while j < MAX_BIT and cnt[j] == 0:
                        j += 1
                    if j == MAX_BIT:
                        return -1  # impossible
                    # Perform (j - i) split operations on one element of size 2^j
                    ops += j - i
                    cnt[j] -= 1
                    # Splitting creates 2^{j-i} pieces of size 2^i
                    cnt[i] += 1 << (j - i)
                    # Use one of them for the current bit
                    cnt[i] -= 1
            # After handling the target bit, combine pairs of current size into next size
            # because two 2^i can form one 2^{i+1}
            if i + 1 < MAX_BIT:
                cnt[i + 1] += cnt[i] // 2
        return ops
