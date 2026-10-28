from typing import List

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # Count how many numbers we have for each power of two (0..30)
        MAX_BIT = 31  # since nums[i] <= 2^30 and target < 2^31
        cnt = [0] * MAX_BIT
        for x in nums:
            # x is guaranteed to be a power of two
            p = x.bit_length() - 1
            cnt[p] += 1

        ops = 0
        # Process bits from low to high
        for i in range(MAX_BIT):
            # If the i-th bit is required by target
            if (target >> i) & 1:
                if cnt[i] > 0:
                    # Use one existing element of 2^i
                    cnt[i] -= 1
                else:
                    # Need to split a larger power of two
                    j = i + 1
                    while j < MAX_BIT and cnt[j] == 0:
                        j += 1
                    if j == MAX_BIT:
                        # No larger element can be split -> impossible
                        return -1
                    # Split down from power j to i
                    while j > i:
                        # Take one element of 2^j and split it into two of 2^{j-1}
                        cnt[j] -= 1
                        cnt[j - 1] += 2
                        ops += 1
                        j -= 1
                    # After splitting, we have at least one 2^i
                    cnt[i] -= 1
            # After handling the current bit, combine pairs of 2^i into 2^{i+1}
            if i + 1 < MAX_BIT:
                cnt[i + 1] += cnt[i] // 2
        return ops
