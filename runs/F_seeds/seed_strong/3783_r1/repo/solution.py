from typing import *
from functools import lru_cache


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # State: o odd values remain, e even values remain, last placed parity p
        # (1 = odd, 0 = even). Count of valid completions g(o, e, p).
        @lru_cache(maxsize=None)
        def g(o: int, e: int, p: int) -> int:
            if o + e == 0:
                return 1
            if p == 1:
                # next must be even
                return e * g(o, e - 1, 0) if e > 0 else 0
            # p == 0: next must be odd
            return o * g(o - 1, e, 1) if o > 0 else 0

        odd_total = (n + 1) // 2
        even_total = n // 2
        o, e = odd_total, even_total
        remaining = list(range(1, n + 1))  # sorted
        res: List[int] = []
        prev = None  # parity of previous element, None at start
        for _ in range(n):
            chosen = False
            for x in remaining:
                px = x & 1
                if prev is not None and px == prev:
                    continue
                # count completions if x is placed now
                if px == 1:
                    cnt = g(o - 1, e, 1)
                else:
                    cnt = g(o, e - 1, 0)
                if k > cnt:
                    k -= cnt
                    continue
                # choose x
                remaining.remove(x)
                if px == 1:
                    o -= 1
                else:
                    e -= 1
                res.append(x)
                prev = px
                chosen = True
                break
            if not chosen:
                return []
        return res
