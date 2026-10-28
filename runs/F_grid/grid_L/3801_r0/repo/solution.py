from functools import lru_cache


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count(n: int) -> int:
            # count beautiful numbers in [1, n]
            if n <= 0:
                return 0
            digits = list(map(int, str(n)))
            L = len(digits)

            # memo for free (non-tight, started) suffixes: key (pos, sum, prod)
            @lru_cache(maxsize=None)
            def free(pos: int, s: int, p: int) -> int:
                # number of ways to fill positions pos..L-1 freely, final
                # sum s and product p; returns count of beautiful completions
                if pos == L:
                    return 1 if p % s == 0 else 0
                total = 0
                for d in range(10):
                    total += free(pos + 1, s + d, p * d)
                return total

            def dfs(pos: int, s: int, p: int, tight: bool, started: bool) -> int:
                if pos == L:
                    if not started:
                        return 0
                    return 1 if p % s == 0 else 0
                if not tight and started:
                    return free(pos, s, p)
                limit = digits[pos] if tight else 9
                total = 0
                for d in range(limit + 1):
                    nt = tight and d == limit
                    if not started and d == 0:
                        total += dfs(pos + 1, 0, 1, nt, False)
                    else:
                        total += dfs(pos + 1, s + d, p * d, nt, True)
                return total

            result = dfs(0, 0, 1, True, False)
            return result

        return count(r) - count(l - 1)
