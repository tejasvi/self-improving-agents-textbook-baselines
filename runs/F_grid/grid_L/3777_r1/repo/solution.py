from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # Partial alternating sums are bounded by sum(nums) <= 150 * 12 = 1800 in abs value.
        OFF = 1800
        if abs(k) > OFF:
            return -1
        OVER = limit + 1  # sentinel: product exceeds limit (may still drop to 0 if a 0 is added)

        def mul(p, x):
            if x == 0:
                return 0
            if p == OVER:
                return OVER
            q = p * x
            return q if q <= limit else OVER

        # dp[(parity, product)] = bitmask over (sum + OFF) of achievable alternating sums
        # for non-empty subsequences. parity = length % 2.
        dp = {}
        for x in nums:
            new = {}
            # Skip x: keep all existing subsequences.
            for key, mask in dp.items():
                new[key] = new.get(key, 0) | mask
            # Start a new subsequence with x (sign +).
            key = (1, mul(1, x))
            new[key] = new.get(key, 0) | (1 << (OFF + x))
            # Extend existing subsequences with x.
            for (par, prod), mask in dp.items():
                np_ = mul(prod, x)
                if par == 0:
                    m = mask << x   # next element gets sign +
                    nk = (1, np_)
                else:
                    m = mask >> x   # next element gets sign -
                    nk = (0, np_)
                new[nk] = new.get(nk, 0) | m
            dp = new
        best = -1
        bit = OFF + k
        for (par, prod), mask in dp.items():
            if prod != OVER and (mask >> bit) & 1 and prod > best:
                best = prod
        return best
