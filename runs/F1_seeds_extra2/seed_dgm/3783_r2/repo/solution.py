from functools import lru_cache
from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # last parity: 0 = even, 1 = odd, 2 = none (start)
        @lru_cache(maxsize=None)
        def count(o: int, e: int, last: int) -> int:
            if o == 0 and e == 0:
                return 1
            total = 0
            if o > 0 and last != 1:
                total += o * count(o - 1, e, 1)
            if e > 0 and last != 0:
                total += e * count(o, e - 1, 0)
            return total

        odds = (n + 1) // 2
        evens = n // 2
        if k > count(odds, evens, 2):
            return []

        remaining = list(range(1, n + 1))
        result = []
        last = 2
        for _ in range(n):
            chosen_idx = None
            for idx, v in enumerate(remaining):
                q = v & 1
                if last != 2 and q == last:
                    continue
                o = sum(1 for x in remaining if x & 1) - q
                e = sum(1 for x in remaining if not x & 1) - (1 - q)
                c = count(o, e, q)
                if k <= c:
                    chosen_idx = idx
                    last = q
                    break
                k -= c
            v = remaining.pop(chosen_idx)
            result.append(v)
        return result
