from typing import List
from functools import lru_cache


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # g(o, e, last_parity): number of ways to arrange o odd and e even
        # remaining numbers so that they alternate, given the previously
        # placed element has parity last_parity (1 = odd, 0 = even).
        @lru_cache(maxsize=None)
        def g(o, e, last):
            if o == 0 and e == 0:
                return 1
            total = 0
            if last == 0:  # next must be odd
                if o > 0:
                    total = o * g(o - 1, e, 1)
            else:  # next must be even
                if e > 0:
                    total = e * g(o, e - 1, 0)
            return total

        remaining = list(range(1, n + 1))
        result = []
        last = None  # parity of last placed element, None at start
        for _ in range(n):
            chosen = False
            for idx, v in enumerate(remaining):
                p = v & 1
                if last is not None and p == last:
                    continue
                o = sum(1 for x in remaining if x & 1) - p
                e = sum(1 for x in remaining if not (x & 1)) - (1 - p)
                cnt = g(o, e, p)
                if k <= cnt:
                    result.append(v)
                    remaining.pop(idx)
                    last = p
                    chosen = True
                    break
                k -= cnt
            if not chosen:
                return []
        return result
