# Write your solution here. Read from stdin, write to stdout.

import sys
import math

def integer_cuberoot_floor(n: int) -> int:
    """Return floor(cuberoot(n)) using integer binary search."""
    lo, hi = 0, int(10**6) + 5  # since (1e6)^3 = 1e18, safe upper bound
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * mid * mid <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    # Upper bound for d = x - y : d^3 <= N
    max_d = integer_cuberoot_floor(N) + 2
    for d in range(1, max_d + 1):
        if N % d != 0:
            continue
        S = N // d
        # delta = 12*S - 3*d*d must be a perfect square
        delta = 12 * S - 3 * d * d
        if delta <= 0:
            continue
        sqrt_delta = math.isqrt(delta)
        if sqrt_delta * sqrt_delta != delta:
            continue
        # y = (sqrt_delta - 3*d) / 6 must be positive integer
        if (sqrt_delta - 3 * d) % 6 != 0:
            continue
        y = (sqrt_delta - 3 * d) // 6
        if y <= 0:
            continue
        x = y + d
        if x * x * x - y * y * y == N:
            print(x, y)
            return
    print(-1)

if __name__ == "__main__":
    solve()
