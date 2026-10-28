from math import gcd
from typing import List


class Solution:
    def findKthSmallest(self, coins: List[int], k: int) -> int:
        n = len(coins)
        # Upper bound: the smallest coin alone yields k-th multiple at k * min(coins).
        hi = k * min(coins)
        cap = hi + 1  # any lcm above hi contributes zero multiples in range

        # Inclusion-exclusion terms: for each nonempty subset, lcm and sign.
        lcms = [1] * (1 << n)
        terms = []  # (lcm, sign) for nonempty subsets with lcm <= hi
        for mask in range(1, 1 << n):
            low = mask & -mask
            i = low.bit_length() - 1
            prev = lcms[mask ^ low]
            if prev >= cap:
                val = cap
            else:
                g = gcd(prev, coins[i])
                val = prev // g * coins[i]
                if val > hi:
                    val = cap
            lcms[mask] = val
            if val < cap:
                sign = 1 if bin(mask).count("1") % 2 == 1 else -1
                terms.append((val, sign))

        def count(x: int) -> int:
            total = 0
            for l, s in terms:
                total += s * (x // l)
            return total

        lo = 1
        while lo < hi:
            mid = (lo + hi) // 2
            if count(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo
