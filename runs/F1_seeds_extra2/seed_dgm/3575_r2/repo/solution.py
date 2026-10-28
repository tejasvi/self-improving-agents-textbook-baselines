from typing import List


class Solution:
    def maxValue(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def prefix_or_sets(seq):
            # sets[j] is a bitmask over OR-values (< 128): bit v set iff value v
            # is the OR of some j-element subsequence of the processed prefix.
            # Returns res where res[m] = bitmask of OR values for exactly k
            # elements chosen from seq[:m].
            sets = [0] * (k + 1)
            sets[0] = 1  # OR value 0 with zero elements
            res = [0] * (len(seq) + 1)
            res[0] = sets[k]
            for idx, x in enumerate(seq):
                for j in range(k, 0, -1):
                    src = sets[j - 1]
                    if src:
                        new = 0
                        s = src
                        while s:
                            low = s & -s
                            v = low.bit_length() - 1
                            new |= 1 << (v | x)
                            s ^= low
                        sets[j] |= new
                res[idx + 1] = sets[k]
            return res

        left = prefix_or_sets(nums)                 # left[m]: from nums[:m]
        right_rev = prefix_or_sets(nums[::-1])      # right_rev[t]: from last t elements

        def bits(mask):
            out = []
            while mask:
                low = mask & -mask
                out.append(low.bit_length() - 1)
                mask ^= low
            return out

        best = -1
        for m in range(k, n - k + 1):
            L = left[m]
            R = right_rev[n - m]
            if not L or not R:
                continue
            a = bits(L)
            b = bits(R)
            for x in a:
                for y in b:
                    if x ^ y > best:
                        best = x ^ y
        return best
