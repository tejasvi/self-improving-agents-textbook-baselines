from typing import List
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        def count(o: int, e: int, p: int) -> int:
            # o odd / e even values remain; p = parity of last placed element
            L = o + e
            if L == 0:
                return 1
            q = 1 - p  # parity of the next element (forced)
            if q == 1:
                ok = (o == (L + 1) // 2 and e == L // 2)
            else:
                ok = (e == (L + 1) // 2 and o == L // 2)
            return factorial(o) * factorial(e) if ok else 0

        odds = (n + 1) // 2
        evens = n // 2
        total = 0
        for v in range(1, n + 1):
            o = odds - (v % 2)
            e = evens - (1 - v % 2)
            total += count(o, e, v % 2)
        if k > total:
            return []

        rem = list(range(1, n + 1))
        res = []
        p = None
        for _ in range(n):
            o_rem = sum(1 for x in rem if x % 2 == 1)
            e_rem = len(rem) - o_rem
            for v in rem:
                if p is not None and v % 2 == p:
                    continue
                pv = v % 2
                o = o_rem - pv
                e = e_rem - (1 - pv)
                c = count(o, e, pv)
                if k <= c:
                    res.append(v)
                    rem.remove(v)
                    p = pv
                    break
                k -= c
            else:
                return []
        return res
