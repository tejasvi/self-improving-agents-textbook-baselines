from typing import List
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        def count(a: int, b: int, next_parity: int) -> int:
            # a: remaining odd values, b: remaining even values,
            # next_parity: parity required for the next element (1=odd, 0=even)
            m = a + b
            if m == 0:
                return 1
            if next_parity == 1:
                if a != (m + 1) // 2 or b != m // 2:
                    return 0
            else:
                if b != (m + 1) // 2 or a != m // 2:
                    return 0
            return factorial(a) * factorial(b)

        odd_cnt = (n + 1) // 2
        even_cnt = n // 2
        used = [False] * (n + 1)
        total = 0
        for v in range(1, n + 1):
            a = odd_cnt - (v % 2)
            b = even_cnt - (1 - v % 2)
            total += count(a, b, 1 - (v % 2))
        if k > total:
            return []

        res = []
        last = None  # parity of last placed element
        a, b = odd_cnt, even_cnt  # remaining counts
        for _ in range(n):
            for v in range(1, n + 1):
                if used[v]:
                    continue
                p = v % 2
                if last is not None and p == last:
                    continue
                na = a - p
                nb = b - (1 - p)
                c = count(na, nb, 1 - p)
                if k <= c:
                    used[v] = True
                    res.append(v)
                    a, b, last = na, nb, p
                    break
                k -= c
        return res
