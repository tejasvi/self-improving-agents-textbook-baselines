from typing import *
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Number of ways to complete given o odd and e even numbers remain,
        # where the next element must have parity `need` (0 = even, 1 = odd,
        # None = any). Adjacent elements must differ in parity, so the parity
        # pattern is forced once the starting parity is fixed; odds and evens
        # then arrange freely among their slots.
        def completions(o: int, e: int, need) -> int:
            m = o + e
            if m == 0:
                return 1
            if need is None:
                if o - e in (-1, 0, 1):
                    # Pattern is determined by start parity; both starts may be valid.
                    total = 0
                    if o - e in (0, 1):
                        total += factorial(o) * factorial(e)
                    if e - o in (0, 1):
                        total += factorial(o) * factorial(e)
                    return total
                return 0
            if need == 1:
                return factorial(o) * factorial(e) if o - e in (0, 1) else 0
            return factorial(o) * factorial(e) if e - o in (0, 1) else 0

        remaining = list(range(1, n + 1))
        res: List[int] = []
        need = None
        for _ in range(n):
            chosen = None
            for x in remaining:
                if need is not None and (x % 2) != need:
                    continue
                o = sum(1 for y in remaining if y % 2 == 1) - (x % 2 == 1)
                e = sum(1 for y in remaining if y % 2 == 0) - (x % 2 == 0)
                # Next element must have opposite parity of x.
                cnt = completions(o, e, 1 - (x % 2))
                if k <= cnt:
                    chosen = x
                    break
                k -= cnt
            if chosen is None:
                return []
            res.append(chosen)
            remaining.remove(chosen)
            need = 1 - (chosen % 2)
        return res
