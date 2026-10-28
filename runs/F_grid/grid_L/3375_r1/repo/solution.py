from typing import List
from math import gcd


class Solution:
    def findKthSmallest(self, coins: List[int], k: int) -> int:
        n = len(coins)
        # The k-th multiple of the smallest coin is an upper bound on the answer.
        hi = min(coins) * k

        # Inclusion-exclusion over nonempty subsets: count(x) = sum over subsets
        # S of (-1)^(|S|+1) * floor(x / lcm(S)). Keep only lcms <= hi.
        lcms = [1] * (1 << n)
        terms = []  # (lcm, sign)
        for mask in range(1, 1 << n):
            low = mask & -mask
            i = low.bit_length() - 1
            rest = mask ^ low
            if rest == 0:
                cur = coins[i]
            else:
                p = lcms[rest]
                cur = p * coins[i] // gcd(p, coins[i])
            lcms[mask] = cur
            if cur <= hi:
                sign = 1 if bin(mask).count("1") % 2 == 1 else -1
                terms.append((cur, sign))

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
