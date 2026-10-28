from functools import lru_cache
from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # g(o, e, p): number of ways to arrange the remaining o odd and e even
        # values, given the previously placed element has parity p (1 = odd, 0 = even),
        # so that no two adjacent elements share parity.
        @lru_cache(maxsize=None)
        def g(o, e, p):
            if o == 0 and e == 0:
                return 1
            if p == 1:  # next must be even
                return e * g(o, e - 1, 0) if e > 0 else 0
            else:  # next must be odd
                return o * g(o - 1, e, 1) if o > 0 else 0

        odds = (n + 1) // 2
        evens = n // 2
        # Total count of alternating permutations (first element free).
        total = 0
        for v in range(1, n + 1):
            if v % 2:
                total += g(odds - 1, evens, 1)
            else:
                total += g(odds, evens - 1, 0)
        if k > total:
            return []

        remaining = list(range(1, n + 1))
        result = []
        last = None
        for _ in range(n):
            o = sum(1 for x in remaining if x % 2)
            e = len(remaining) - o
            chosen = None
            for idx, v in enumerate(remaining):
                p = v % 2
                if last is not None and p == last:
                    continue
                if p:
                    cnt = g(o - 1, e, 1)
                else:
                    cnt = g(o, e - 1, 0)
                if k <= cnt:
                    chosen = idx
                    break
                k -= cnt
            v = remaining.pop(chosen)
            result.append(v)
            last = v % 2
        return result
