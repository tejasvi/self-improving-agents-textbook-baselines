from typing import List
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        def ways(o: int, e: int, s: int) -> int:
            # number of alternating arrangements of o odds and e evens
            # whose first element has parity s (1 = odd, 0 = even)
            total = o + e
            if total == 0:
                return 1
            need_odd = (total + 1) // 2 if s == 1 else total // 2
            if o != need_odd:
                return 0
            return factorial(o) * factorial(e)

        remaining = list(range(1, n + 1))
        o = (n + 1) // 2
        e = n // 2

        # total number of alternating permutations
        total = ways(o, e, 1) + ways(o, e, 0)
        if k > total:
            return []

        res = []
        last_parity = None  # parity of last placed element
        for _ in range(n):
            chosen_idx = -1
            for idx, x in enumerate(remaining):
                q = x & 1
                if last_parity is not None and q == last_parity:
                    continue
                no = o - q
                ne = e - (1 - q)
                cnt = ways(no, ne, 1 - q)
                if k <= cnt:
                    chosen_idx = idx
                    break
                k -= cnt
            x = remaining.pop(chosen_idx)
            res.append(x)
            if x & 1:
                o -= 1
            else:
                e -= 1
            last_parity = x & 1
        return res
