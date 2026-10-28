from typing import List

class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        # Count occurrences of each power of two
        MAX_BIT = 31  # sufficient for values up to 2^30 and target up to <2^31
        cnt = [0] * (MAX_BIT + 1)  # extra slot for carry overflow
        for num in nums:
            # num is a power of two, find its exponent
            exp = num.bit_length() - 1
            cnt[exp] += 1

        ops = 0          # total operations performed
        need = 0         # how many units of current power we still need to satisfy target
        for i in range(MAX_BIT):
            # incorporate the i‑th bit of target into the need
            need += (target >> i) & 1
            if cnt[i] >= need:
                # we have enough of 2^i to cover the need
                surplus = cnt[i] - need
                # every two surplus items can be merged into one of the next higher power
                cnt[i + 1] += surplus // 2
                need = 0
            else:
                # not enough; we must split a larger power
                # keep splitting until we have enough at level i
                while cnt[i] < need:
                    # locate the nearest higher power that exists
                    j = i + 1
                    while j < len(cnt) and cnt[j] == 0:
                        j += 1
                    if j == len(cnt):
                        return -1  # impossible to obtain required sum
                    # split one element of size 2^j down to size 2^{j-1}
                    while j > i:
                        cnt[j] -= 1
                        cnt[j - 1] += 2
                        ops += 1
                        j -= 1
                # after the loop we have cnt[i] >= need
                surplus = cnt[i] - need
                cnt[i + 1] += surplus // 2
                need = 0
        # After processing all bits, if any need remains it means target required a higher bit than we can provide
        return ops if need == 0 else -1
