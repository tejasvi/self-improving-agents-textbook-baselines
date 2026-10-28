from functools import lru_cache
from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # State: a = remaining odd count, b = remaining even count,
        # last = parity of previously placed value (0 even, 1 odd, 2 none).
        @lru_cache(maxsize=None)
        def count(a: int, b: int, last: int) -> int:
            if a == 0 and b == 0:
                return 1
            total = 0
            # next value must have parity different from last
            if last != 1 and a > 0:  # next odd, allowed if last is even or none
                total += a * count(a - 1, b, 1)
            if last != 0 and b > 0:  # next even, allowed if last is odd or none
                total += b * count(a, b - 1, 0)
            return total

        n_odd = (n + 1) // 2
        n_even = n // 2
        total = count(n_odd, n_even, 2)
        if k > total:
            return []

        used = [False] * (n + 1)
        a, b, last = n_odd, n_even, 2
        res = []
        for _ in range(n):
            for v in range(1, n + 1):
                if used[v]:
                    continue
                p = v & 1
                if last != 2 and p == last:
                    continue
                if p == 1:
                    ways = count(a - 1, b, 1)
                else:
                    ways = count(a, b - 1, 0)
                if k <= ways:
                    used[v] = True
                    res.append(v)
                    if p == 1:
                        a -= 1
                    else:
                        b -= 1
                    last = p
                    break
                k -= ways
        return res
