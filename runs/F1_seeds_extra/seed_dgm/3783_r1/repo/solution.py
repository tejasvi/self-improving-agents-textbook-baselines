from functools import lru_cache
from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # last: 0 = even, 1 = odd
        @lru_cache(maxsize=None)
        def f(o: int, e: int, last: int) -> int:
            # number of ways to arrange o odd and e even remaining values
            # given the previous element has parity `last`
            if o == 0 and e == 0:
                return 1
            total = 0
            if last == 1:
                if e > 0:
                    total = e * f(o, e - 1, 0)
            else:
                if o > 0:
                    total = o * f(o - 1, e, 1)
            return total

        O = (n + 1) // 2
        E = n // 2
        remaining = list(range(1, n + 1))
        o, e = O, E
        last = -1  # no previous element
        result = []

        for _ in range(n):
            chosen = False
            for v in remaining:
                p = v & 1
                if last != -1 and p == last:
                    continue
                if p == 1:
                    cnt = f(o - 1, e, 1)
                else:
                    cnt = f(o, e - 1, 0)
                if k <= cnt:
                    result.append(v)
                    remaining.remove(v)
                    if p == 1:
                        o -= 1
                    else:
                        e -= 1
                    last = p
                    chosen = True
                    break
                k -= cnt
            if not chosen:
                return []
        return result
