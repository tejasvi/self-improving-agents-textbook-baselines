from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count(n: int) -> int:
            # Number of beautiful integers in [1, n].
            if n <= 0:
                return 0
            digits = list(map(int, str(n)))
            m = len(digits)

            @lru_cache(maxsize=None)
            def dp(pos, s, p, tight, started):
                if pos == m:
                    if not started:
                        return 0
                    return 1 if p % s == 0 else 0
                limit = digits[pos] if tight else 9
                total = 0
                for d in range(limit + 1):
                    nt = tight and d == limit
                    if not started and d == 0:
                        total += dp(pos + 1, 0, 1, nt, False)
                    else:
                        total += dp(pos + 1, s + d, p * d, nt, True)
                return total

            result = dp(0, 0, 1, True, False)
            dp.cache_clear()
            return result

        return count(r) - count(l - 1)
