from typing import List
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Number of alternating completions given `a` odd and `b` even values
        # remain and the next element must have parity `nxt` (1 = odd, 0 = even).
        def count(a: int, b: int, nxt: int) -> int:
            if a == 0 and b == 0:
                return 1
            if nxt == 1:
                if a - b not in (0, 1):
                    return 0
            else:
                if b - a not in (0, 1):
                    return 0
            return factorial(a) * factorial(b)

        odds = (n + 1) // 2
        evens = n // 2
        if count(odds, evens, 1) + count(odds, evens, 0) < k:
            return []

        used = [False] * (n + 1)
        res = []
        a, b = odds, evens
        last = None  # parity of last placed element
        for _ in range(n):
            for v in range(1, n + 1):
                if used[v]:
                    continue
                p = v & 1
                if last is not None and p == last:
                    continue
                na, nb = (a - 1, b) if p == 1 else (a, b - 1)
                c = count(na, nb, 1 - p)
                if k <= c:
                    used[v] = True
                    res.append(v)
                    a, b, last = na, nb, p
                    break
                k -= c
        return res
