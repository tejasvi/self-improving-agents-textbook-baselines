from typing import *
from functools import lru_cache
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Parity pattern counts: g(o, e, last) = number of parity patterns using
        # o odd and e even slots, alternating, whose first element differs in
        # parity from `last` (0 = odd, 1 = even, 2 = none).
        # Each pattern corresponds to o! * e! actual permutations.
        @lru_cache(maxsize=None)
        def g(o: int, e: int, last: int) -> int:
            if o == 0 and e == 0:
                return 1
            total = 0
            if o > 0 and last != 0:
                total += g(o - 1, e, 0)
            if e > 0 and last != 1:
                total += g(o, e - 1, 1)
            return total

        def full(o: int, e: int, last: int) -> int:
            return g(o, e, last) * factorial(o) * factorial(e)

        odds = (n + 1) // 2
        evens = n // 2
        if k > full(odds, evens, 2):
            return []

        remaining = list(range(1, n + 1))  # sorted; remaining values per parity
        res = []
        o, e, last = odds, evens, 2
        for _ in range(n):
            for idx, v in enumerate(remaining):
                p = 0 if v % 2 == 1 else 1
                if p == last:
                    continue
                if p == 0:
                    cnt = full(o - 1, e, 0)
                else:
                    cnt = full(o, e - 1, 1)
                if k <= cnt:
                    res.append(v)
                    remaining.pop(idx)
                    if p == 0:
                        o -= 1
                    else:
                        e -= 1
                    last = p
                    break
                k -= cnt
        return res
