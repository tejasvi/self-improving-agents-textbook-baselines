from typing import *
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        fact = [1] * (n + 2)
        for i in range(1, n + 2):
            fact[i] = fact[i - 1] * i

        def ways(o: int, e: int, first: int) -> int:
            # number of alternating-parity arrangements of o odds and e evens
            # whose first element has parity `first` (1 = odd, 0 = even)
            L = o + e
            if L == 0:
                return 1
            if first == 1:
                if o == (L + 1) // 2 and e == L // 2:
                    return fact[o] * fact[e]
            else:
                if e == (L + 1) // 2 and o == L // 2:
                    return fact[o] * fact[e]
            return 0

        remaining = list(range(1, n + 1))
        odd = (n + 1) // 2
        even = n // 2
        # total count check
        total = ways(odd, even, 1) + ways(odd, even, 0)
        if k > total:
            return []

        res = []
        last = -1  # parity of last placed element, -1 if none
        for _ in range(n):
            chosen = False
            for idx, v in enumerate(remaining):
                p = v & 1
                if last != -1 and p == last:
                    continue
                no = odd - (1 if p == 1 else 0)
                ne = even - (1 if p == 0 else 0)
                cnt = ways(no, ne, 1 - p)
                if k <= cnt:
                    res.append(v)
                    remaining.pop(idx)
                    odd, even = no, ne
                    last = p
                    chosen = True
                    break
                k -= cnt
            if not chosen:
                return []
        return res
