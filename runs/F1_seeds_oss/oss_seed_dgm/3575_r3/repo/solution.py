from typing import List

class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)
        max_or = 128  # values are < 2^7, so possible OR results are 0..127
        # Prefix DP: pref[i][c] = bitmask of achievable OR values using exactly c elements from first i elements
        pref = [[0] * (k + 1) for _ in range(n + 1)]
        pref[0][0] = 1  # only OR value 0 with 0 elements
        for i in range(1, n + 1):
            val = nums[i - 1]
            for c in range(0, k + 1):
                # skip current element
                pref[i][c] = pref[i - 1][c]
                if c > 0:
                    bits = pref[i - 1][c - 1]
                    while bits:
                        low = bits & -bits
                        prev_or = low.bit_length() - 1
                        new_or = prev_or | val
                        pref[i][c] |= 1 << new_or
                        bits ^= low
        # Suffix DP: suff[i][c] = bitmask of achievable OR values using exactly c elements from suffix starting at i
        suff = [[0] * (k + 1) for _ in range(n + 1)]
        suff[n][0] = 1
        for i in range(n - 1, -1, -1):
            val = nums[i]
            for c in range(0, k + 1):
                # skip current element
                suff[i][c] = suff[i + 1][c]
                if c > 0:
                    bits = suff[i + 1][c - 1]
                    while bits:
                        low = bits & -bits
                        prev_or = low.bit_length() - 1
                        new_or = prev_or | val
                        suff[i][c] |= 1 << new_or
                        bits ^= low
        # Combine prefix and suffix results. The split point i means first i elements are considered for the first half.
        # We need at least k elements before i and at least k elements after i.
        best = 0
        for i in range(k, n - k + 1):
            mask_a = pref[i][k]
            mask_b = suff[i][k]
            if mask_a == 0 or mask_b == 0:
                continue
            # Enumerate all possible OR values from both halves (0..127)
            # Since the range is tiny, a double loop is acceptable.
            a_bits = mask_a
            while a_bits:
                low_a = a_bits & -a_bits
                a_val = low_a.bit_length() - 1
                b_bits = mask_b
                while b_bits:
                    low_b = b_bits & -b_bits
                    b_val = low_b.bit_length() - 1
                    xor_val = a_val ^ b_val
                    if xor_val > best:
                        best = xor_val
                    b_bits ^= low_b
                a_bits ^= low_a
        return best
