# Solution for counting distinct perfect powers up to N (b >= 2).
# Uses Python's arbitrary-precision integers and math.isqrt for exact integer roots.

import sys
import math


def integer_cuberoot(n: int) -> int:
    """Return floor(cuberoot(n)). Uses binary search for exact integer result."""
    if n < 8:
        return 1 if n >= 1 else 0
    lo, hi = 0, int(n ** (1/3)) + 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid
    return lo


def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])

    # Count all squares (including 1).
    squares_cnt = math.isqrt(N)

    # Set for perfect powers with exponent >= 3.
    pp_set = set()
    # Upper bound for base a: if a^3 <= N then a <= floor(N^{1/3}).
    a_max = integer_cuberoot(N)
    for a in range(2, a_max + 1):
        val = a * a * a  # a^3
        while val <= N:
            pp_set.add(val)
            # Prevent overflow in next multiplication (Python handles it, but we break when it would exceed N).
            if val > N // a:
                break
            val *= a

    # Remove those that are perfect squares to avoid double counting.
    overlap = 0
    for v in pp_set:
        r = math.isqrt(v)
        if r * r == v:
            overlap += 1

    answer = squares_cnt + len(pp_set) - overlap
    print(answer)


if __name__ == "__main__":
    solve()
