from typing import *


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # W(a, b, p): number of ways to arrange a remaining odd and b remaining
        # even values (distinct labels) so that the sequence alternates in
        # parity and the first element has parity opposite to p (p = parity of
        # the previously placed element, 1 = odd, 0 = even).
        W = {}

        def w(a: int, b: int, p: int) -> int:
            if a == 0 and b == 0:
                return 1
            key = (a, b, p)
            if key in W:
                return W[key]
            q = 1 - p
            total = 0
            if q == 1:
                if a > 0:
                    total = a * w(a - 1, b, 1)
            else:
                if b > 0:
                    total = b * w(a, b - 1, 0)
            W[key] = total
            return total

        odd_left = (n + 1) // 2
        even_left = n // 2
        used = [False] * (n + 1)
        result = []
        last_parity = None  # None means no previous element
        for pos in range(n):
            chosen = None
            for v in range(1, n + 1):
                if used[v]:
                    continue
                if last_parity is not None and (v & 1) == last_parity:
                    continue
                # remaining counts after placing v
                a = odd_left - (1 if v & 1 else 0)
                b = even_left - (0 if v & 1 else 1)
                cnt = w(a, b, v & 1)
                if k <= cnt:
                    chosen = v
                    break
                k -= cnt
            if chosen is None:
                return []
            v = chosen
            used[v] = True
            if v & 1:
                odd_left -= 1
            else:
                even_left -= 1
            last_parity = v & 1
            result.append(v)
        return result
