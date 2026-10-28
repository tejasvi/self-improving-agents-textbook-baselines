from functools import lru_cache


class Solution:
    def numberOfBeautifulIntegers(self, low: int, high: int, k: int) -> int:
        def count(n: int) -> int:
            # number of beautiful integers in [1, n]
            if n <= 0:
                return 0
            digits = list(map(int, str(n)))
            L = len(digits)

            @lru_cache(maxsize=None)
            def dp(pos, diff, rem, tight, started):
                if pos == L:
                    return 1 if started and diff == 0 and rem == 0 else 0
                limit = digits[pos] if tight else 9
                total = 0
                for d in range(limit + 1):
                    nt = tight and d == limit
                    if not started and d == 0:
                        total += dp(pos + 1, 0, 0, nt, False)
                        continue
                    nd = diff + (1 if d % 2 == 0 else -1)
                    nr = (rem * 10 + d) % k
                    total += dp(pos + 1, nd, nr, nt, True)
                return total

            res = dp(0, 0, 0, True, False)
            dp.cache_clear()
            return res

        return count(high) - count(low - 1)
