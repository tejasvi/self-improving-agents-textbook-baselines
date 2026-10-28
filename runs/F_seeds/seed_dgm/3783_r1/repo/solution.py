from typing import List
from math import factorial


class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        def completions(a: int, b: int, need_odd: bool) -> int:
            # a: remaining odd count, b: remaining even count
            # need_odd: parity required for the next element (None-like handled by caller)
            m = a + b
            if m == 0:
                return 1
            # alternating pattern starting with required parity
            if need_odd:
                ok = (a == (m + 1) // 2 and b == m // 2)
            else:
                ok = (b == (m + 1) // 2 and a == m // 2)
            return factorial(a) * factorial(b) if ok else 0

        used = [False] * (n + 1)
        odd_left = (n + 1) // 2
        even_left = n // 2
        result = []
        last_parity = None  # None means no previous element
        for _ in range(n):
            chosen = False
            for v in range(1, n + 1):
                if used[v]:
                    continue
                is_odd = (v % 2 == 1)
                if last_parity is not None and is_odd == last_parity:
                    continue
                # place v
                a = odd_left - (1 if is_odd else 0)
                b = even_left - (0 if is_odd else 1)
                # next element must have parity opposite to v
                c = completions(a, b, need_odd=not is_odd)
                if k <= c:
                    used[v] = True
                    result.append(v)
                    odd_left, even_left = a, b
                    last_parity = is_odd
                    chosen = True
                    break
                k -= c
            if not chosen:
                return []
        return result
