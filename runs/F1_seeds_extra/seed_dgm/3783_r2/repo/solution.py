from functools import lru_cache
from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # last: 0 = nothing placed yet, 1 = last placed is odd, 2 = last placed is even
        @lru_cache(maxsize=None)
        def f(o: int, e: int, last: int) -> int:
            if o == 0 and e == 0:
                return 1
            total = 0
            if last != 1 and o > 0:
                # next element is odd: choose any of o odds
                total += o * f(o - 1, e, 1)
            if last != 2 and e > 0:
                total += e * f(o, e - 1, 2)
            return total

        odds = (n + 1) // 2
        evens = n // 2
        if k > f(odds, evens, 0):
            return []

        remaining = list(range(1, n + 1))
        result = []
        last = 0
        for _ in range(n):
            for idx, x in enumerate(remaining):
                p = 1 if x % 2 == 1 else 2
                if last != 0 and p == last:
                    continue
                o = sum(1 for y in remaining if y % 2 == 1)
                e = len(remaining) - o
                if p == 1:
                    o -= 1
                else:
                    e -= 1
                cnt = f(o, e, p)
                if k <= cnt:
                    result.append(x)
                    remaining.pop(idx)
                    last = p
                    break
                k -= cnt
        return result
