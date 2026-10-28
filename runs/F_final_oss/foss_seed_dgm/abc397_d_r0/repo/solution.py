# Write your solution here. Read from stdin, write to stdout.

import sys
import math

def integer_cuberoot_floor(n: int) -> int:
    """Return the greatest integer r such that r^3 <= n."""
    # Initial approximation using float, safe for n up to 1e18
    r = int(round(n ** (1/3)))
    # Adjust because of rounding errors
    while (r + 1) ** 3 <= n:
        r += 1
    while r ** 3 > n:
        r -= 1
    return r

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    max_d = integer_cuberoot_floor(N) + 1  # include possible rounding edge
    for d in range(1, max_d + 1):
        if N % d != 0:
            continue
        m = N // d
        # discriminant D = 12*m - 3*d^2 = 3*(4*m - d^2)
        D = 12 * m - 3 * d * d
        if D < 0:
            continue
        s = math.isqrt(D)
        if s * s != D:
            continue
        # y = (s - 3d) / 6 must be integer and positive
        if (s - 3 * d) % 6 != 0:
            continue
        y = (s - 3 * d) // 6
        if y <= 0:
            continue
        x = y + d
        print(x, y)
        return
    print(-1)

if __name__ == "__main__":
    solve()
