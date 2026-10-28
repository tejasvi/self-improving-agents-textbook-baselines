from math import factorial
from typing import List


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        def cnt(o: int, e: int, nxt: int) -> int:
            # Number of alternating arrangements using o odds and e evens,
            # whose first element must have parity nxt (1 = odd, 0 = even).
            L = o + e
            if L == 0:
                return 1
            need_first = (L + 1) // 2
            if nxt == 1 and o != need_first:
                return 0
            if nxt == 0 and e != need_first:
                return 0
            return factorial(o) * factorial(e)

        o = (n + 1) // 2
        e = n // 2
        total = cnt(o, e, 1) + cnt(o, e, 0)
        if k > total:
            return []

        result = []
        remaining = list(range(1, n + 1))
        last = None  # parity of last placed element
        k -= 1  # zero-indexed
        for _ in range(n):
            for x in remaining:
                p = x & 1
                if last is not None and p == last:
                    continue
                no = o - p
                ne = e - (1 - p)
                ways = cnt(no, ne, 1 - p)
                if k < ways:
                    result.append(x)
                    remaining.remove(x)
                    o, e = no, ne
                    last = p
                    break
                k -= ways
        return result
