from typing import *
from functools import lru_cache
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # P(a, b, q): number of parity patterns with a odd and b even items,
        # where the first item has parity q (1 = odd, 0 = even), alternating.
        @lru_cache(maxsize=None)
        def P(a: int, b: int, q: int) -> int:
            if a == 0 and b == 0:
                return 1
            if q == 1:
                return P(a - 1, b, 0) if a > 0 else 0
            return P(a, b - 1, 1) if b > 0 else 0

        def completions(a: int, b: int, q: int) -> int:
            # number of arrangements of a specific set with a odd and b even
            # values, first value having parity q
            return P(a, b, q) * factorial(a) * factorial(b)

        remaining = list(range(1, n + 1))
        a = (n + 1) // 2  # odd count
        b = n // 2        # even count

        total = completions(a, b, 1) + completions(a, b, 0)
        if k > total:
            return []

        res = []
        prev = None  # parity of previous element
        while remaining:
            chosen = False
            for idx, v in enumerate(remaining):
                pv = v & 1
                if prev is not None and pv == prev:
                    continue
                na = a - pv
                nb = b - (1 - pv)
                cnt = completions(na, nb, 1 - pv)
                if k <= cnt:
                    res.append(v)
                    remaining.pop(idx)
                    a, b, prev = na, nb, pv
                    chosen = True
                    break
                k -= cnt
            if not chosen:
                return []  # should not happen
        return res
