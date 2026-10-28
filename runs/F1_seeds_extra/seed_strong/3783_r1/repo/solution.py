from typing import *
from math import factorial


def _count_start(o: int, e: int, p: int) -> int:
    """Number of alternating arrangements of a multiset with o odd and e even
    values whose first element has parity p (1 = odd, 0 = even)."""
    if o + e == 0:
        return 1
    if p == 1:
        if o - e in (0, 1):
            return factorial(o) * factorial(e)
        return 0
    if e - o in (0, 1):
        return factorial(o) * factorial(e)
    return 0


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        remaining = list(range(1, n + 1))
        odd = (n + 1) // 2
        even = n // 2
        res = []
        prev_parity = None
        for _ in range(n):
            chosen = None
            for idx, x in enumerate(remaining):
                px = x & 1
                if prev_parity is not None and px == prev_parity:
                    continue
                # Counts of the set after removing x.
                o = odd - (1 if px == 1 else 0)
                e = even - (1 if px == 0 else 0)
                # Next element must have parity opposite to x.
                cnt = _count_start(o, e, 1 - px)
                if k <= cnt:
                    chosen = idx
                    break
                k -= cnt
            if chosen is None:
                return []
            x = remaining.pop(chosen)
            if x & 1:
                odd -= 1
            else:
                even -= 1
            prev_parity = x & 1
            res.append(x)
        return res
