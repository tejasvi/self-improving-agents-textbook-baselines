from functools import lru_cache

MOD = 10**9 + 7


@lru_cache(maxsize=None)
def _free(k: int, prev: int) -> int:
    """Number of digit strings of length k that continue a stepping
    sequence whose last digit is prev (exact, no bound)."""
    if k == 0:
        return 1
    total = 0
    for d in (prev - 1, prev + 1):
        if 0 <= d <= 9:
            total += _free(k - 1, d)
    return total % MOD


def _count_upto(s: str) -> int:
    """Count stepping numbers in [1, int(s)] (exact, before modulo)."""
    n = len(s)
    total = 0
    # Shorter lengths: first digit 1..9.
    for L in range(1, n):
        for d in range(1, 10):
            total += _free(L - 1, d)
    # Same length as s.
    prev = None
    for i in range(n):
        cur = int(s[i])
        start = 1 if i == 0 else 0
        for d in range(start, cur):
            if prev is None or abs(d - prev) == 1:
                total += _free(n - i - 1, d)
        if prev is not None and abs(cur - prev) != 1:
            return total % MOD
        prev = cur
    total += 1  # s itself is a stepping number
    return total % MOD


def _is_stepping(s: str) -> bool:
    return all(abs(int(s[i]) - int(s[i - 1])) == 1 for i in range(1, len(s)))


class Solution:
    def countSteppingNumbers(self, low: str, high: str) -> int:
        res = _count_upto(high) - _count_upto(low)
        if _is_stepping(low):
            res += 1
        return res % MOD
