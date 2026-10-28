from typing import List
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Number of ways to complete a sequence containing `o` odd and `e` even
        # numbers, where the first chosen element must differ in parity from
        # `prev` (prev is None when no constraint applies).
        def count(o: int, e: int, prev):
            m = o + e
            if m == 0:
                return 1
            total = 0
            for q in (0, 1):  # parity of first element of the remainder (1 = odd)
                if prev is not None and q == prev:
                    continue
                # Alternating sequence of length m starting with parity q
                if q == 1:
                    need_o, need_e = (m + 1) // 2, m // 2
                else:
                    need_o, need_e = m // 2, (m + 1) // 2
                if o == need_o and e == need_e:
                    total += factorial(o) * factorial(e)
            return total

        odds = [x for x in range(1, n + 1) if x % 2 == 1]
        evens = [x for x in range(1, n + 1) if x % 2 == 0]
        remaining = set(range(1, n + 1))

        if k > count(len(odds), len(evens), None):
            return []

        result = []
        prev = None
        for _ in range(n):
            o = sum(1 for x in remaining if x % 2 == 1)
            e = len(remaining) - o
            chosen = None
            for x in sorted(remaining):
                p = x % 2
                if prev is not None and p == prev:
                    continue
                o2 = o - (1 if p == 1 else 0)
                e2 = e - (1 if p == 0 else 0)
                c = count(o2, e2, p)
                if k <= c:
                    chosen = x
                    break
                k -= c
            # chosen is always found given the initial feasibility check
            result.append(chosen)
            remaining.remove(chosen)
            prev = chosen % 2
        return result
