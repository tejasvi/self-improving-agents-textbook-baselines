from typing import *
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Once the starting parity is fixed, the parity of every position is
        # forced, so the number of completions depends only on how many odd
        # and even values remain and which parity comes next.
        def ways(odds: int, evens: int, next_odd: bool) -> int:
            length = odds + evens
            if length == 0:
                return 1
            if next_odd:
                need_odd, need_even = (length + 1) // 2, length // 2
            else:
                need_even, need_odd = (length + 1) // 2, length // 2
            if odds != need_odd or evens != need_even:
                return 0
            return factorial(odds) * factorial(evens)

        used = [False] * (n + 1)
        odds = (n + 1) // 2
        evens = n // 2
        res: List[int] = []
        prev_parity = None  # parity (1 = odd) of previous element
        for _ in range(n):
            chosen = False
            for v in range(1, n + 1):
                if used[v]:
                    continue
                vp = v & 1
                if prev_parity is not None and vp == prev_parity:
                    continue
                # remaining counts after using v
                o = odds - (1 if vp == 1 else 0)
                e = evens - (1 if vp == 0 else 0)
                c = ways(o, e, vp == 0)
                if k <= c:
                    used[v] = True
                    res.append(v)
                    odds, evens = o, e
                    prev_parity = vp
                    chosen = True
                    break
                k -= c
            if not chosen:
                return []
        return res
