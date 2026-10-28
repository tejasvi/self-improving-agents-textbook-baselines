# Palindromic Expression Solver
# Reads integer N and prints a palindrome string consisting of digits 1-9 and '*'
# whose evaluated product equals N, or -1 if impossible.

import sys
import math

DIGITS = set('123456789')

def has_no_zero(s: str) -> bool:
    return all(ch in DIGITS for ch in s)

def is_palindrome(s: str) -> bool:
    return s == s[::-1]

def reverse_int(x: int) -> int:
    return int(str(x)[::-1])

def divisors(n: int):
    """Yield all divisors d of n (including 1 and n) in increasing order."""
    limit = int(math.isqrt(n))
    for d in range(1, limit + 1):
        if n % d == 0:
            yield d
            if d * d != n:
                yield n // d

def try_simple(N: int) -> str:
    """Try representations with at most two symmetric layers.
    Returns the string if found, else empty string.
    """
    sN = str(N)
    if is_palindrome(sN) and has_no_zero(sN):
        return sN

    # One outer layer: a * rev(a) possibly with central palindrome c
    for a in divisors(N):
        if a == 0:
            continue
        sa = str(a)
        if not has_no_zero(sa):
            continue
        rev_a = reverse_int(a)
        if rev_a == 0:
            continue
        if not has_no_zero(str(rev_a)):
            continue
        prod = a * rev_a
        if N % prod != 0:
            continue
        rest = N // prod
        # case: just a*rev_a (rest == 1)
        if rest == 1:
            cand = f"{a}*{rev_a}"
            if len(cand) <= 1000:
                return cand
        # case: a * c * rev_a where c is palindrome without zero
        sc = str(rest)
        if is_palindrome(sc) and has_no_zero(sc):
            cand = f"{a}*{sc}*{rev_a}"
            if len(cand) <= 1000:
                return cand
        # Try a second symmetric layer inside the rest
        # We need rest = b * rev(b) * mid (mid may be 1)
        for b in divisors(rest):
            sb = str(b)
            if not has_no_zero(sb):
                continue
            rev_b = reverse_int(b)
            if rev_b == 0 or not has_no_zero(str(rev_b)):
                continue
            prod2 = b * rev_b
            if rest % prod2 != 0:
                continue
            mid = rest // prod2
            if mid == 1:
                cand = f"{a}*{b}*{rev_b}*{rev_a}"
                if len(cand) <= 1000:
                    return cand
            else:
                smid = str(mid)
                if is_palindrome(smid) and has_no_zero(smid):
                    cand = f"{a}*{b}*{smid}*{rev_b}*{rev_a}"
                    if len(cand) <= 1000:
                        return cand
    return ""

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    ans = try_simple(N)
    if ans:
        print(ans)
    else:
        print(-1)

if __name__ == "__main__":
    solve()
