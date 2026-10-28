# Write your solution here. Read from stdin, write to stdout.
import sys, math

def icbrt(n: int) -> int:
    """Return floor cube root of n (n >= 0)."""
    lo, hi = 0, int(10**6) + 2  # since (1e6)^3 = 1e18, safe upper bound
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
    # Iterate over possible a = x - y, which must divide N and a <= cbrt(N)
    max_a = icbrt(N)
    for a in range(1, max_a + 1):
        if N % a != 0:
            continue
        b = N // a  # b = x^2 + x*y + y^2
        # Solve 3x^2 - 3a x + a^2 - b = 0
        D = 12 * b - 3 * a * a  # discriminant = 3*(4b - a^2)
        if D < 0:
            continue
        sqrtD = int(math.isqrt(D))
        if sqrtD * sqrtD != D:
            continue
        # x = (3a + sqrtD) / 6 must be integer
        if (3 * a + sqrtD) % 6 != 0:
            continue
        x = (3 * a + sqrtD) // 6
        y = x - a
        if x > 0 and y > 0 and x**3 - y**3 == N:
            print(x, y)
            return
    print(-1)

if __name__ == "__main__":
    solve()
