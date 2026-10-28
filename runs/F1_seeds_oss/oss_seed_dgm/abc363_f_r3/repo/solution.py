# Palindromic Expression Solver
import sys
from functools import lru_cache

MAX_LEN = 1000

def has_no_zero(num: int) -> bool:
    """Return True if decimal representation of num contains no '0'."""
    return '0' not in str(num)

def is_palindrome_str(s: str) -> bool:
    return s == s[::-1]

def is_palindrome_num(num: int) -> bool:
    s = str(num)
    return is_palindrome_str(s)

@lru_cache(maxsize=None)
def solve_rec(N: int) -> str | None:
    """Return a palindrome expression for N or None.
    The expression must consist of numbers (no zeros) and '*' characters,
    be a palindrome, and have length <= MAX_LEN.
    """
    # Base: single number
    if has_no_zero(N) and is_palindrome_num(N):
        s = str(N)
        if len(s) <= MAX_LEN:
            return s
    # Try outer factor A (A > 1) such that N = A * inner * A   -> inner = N // (A*A)
    limit = int(N ** 0.5) + 1
    for A in range(2, limit):
        if N % (A * A) != 0:
            continue
        if not has_no_zero(A):
            continue
        inner_val = N // (A * A)
        inner_expr = solve_rec(inner_val)
        if inner_expr is None:
            continue
        candidate = f"{A}*{inner_expr}*{A}"
        if len(candidate) <= MAX_LEN and is_palindrome_str(candidate):
            return candidate
    # Try representation as product of equal factors (A repeated m times) where m>=2
    # This yields palindrome because the string "A*A*...*A" is symmetric.
    # We just need A^m == N.
    # Enumerate possible exponents m up to 60 (since 2^60 > 1e18).
    max_m = 60
    for m in range(2, max_m + 1):
        # integer m-th root, using pow with rounding
        a_approx = int(round(N ** (1.0 / m)))
        for a in (a_approx - 1, a_approx, a_approx + 1):
            if a <= 1:
                continue
            if not has_no_zero(a):
                continue
            # fast power check
            if pow(a, m) == N:
                parts = [str(a)] * m
                candidate = '*'.join(parts)
                if len(candidate) <= MAX_LEN and is_palindrome_str(candidate):
                    return candidate
    # No construction found
    return None

def solve():
    data = sys.stdin.read().strip()
    if not data:
        return
    N = int(data)
    ans = solve_rec(N)
    if ans is None:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
