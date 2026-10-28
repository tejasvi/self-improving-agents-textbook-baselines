from functools import lru_cache
from math import factorial
from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Parity-pattern count: a = remaining odd count, b = remaining even count,
        # last = parity of previously placed element (0 even, 1 odd, 2 none).
        @lru_cache(maxsize=None)
        def patterns(a: int, b: int, last: int) -> int:
            if a == 0 and b == 0:
                return 1
            total = 0
            if a > 0 and last != 1:
                total += patterns(a - 1, b, 1)
            if b > 0 and last != 0:
                total += patterns(a, b - 1, 0)
            return total

        def completions(a: int, b: int, last: int) -> int:
            # Each parity pattern corresponds to a! * b! concrete permutations.
            return patterns(a, b, last) * factorial(a) * factorial(b)

        odd_cnt = (n + 1) // 2
        even_cnt = n // 2
        if k > completions(odd_cnt, even_cnt, 2):
            return []

        remaining = list(range(1, n + 1))
        result = []
        last = 2
        for _ in range(n):
            a = sum(1 for v in remaining if v % 2 == 1)
            b = len(remaining) - a
            for idx, v in enumerate(remaining):
                q = v % 2
                if last != 2 and q == last:
                    continue
                # Completions after fixing v at this position
                if q == 1:
                    ways = completions(a - 1, b, 1)
                else:
                    ways = completions(a, b - 1, 0)
                if k <= ways:
                    result.append(v)
                    remaining.pop(idx)
                    last = q
                    break
                k -= ways
        return result
