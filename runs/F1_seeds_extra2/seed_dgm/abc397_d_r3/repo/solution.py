import sys
from math import isqrt


def solve(n):
    # x = y + d, N = d * (3y^2 + 3dy + d^2), and d^3 < N since y >= 1.
    d = 1
    while d * d * d < n:
        if n % d == 0:
            m = n // d - d * d
            # 3y^2 + 3dy - m = 0  ->  y = (s - 3d) / 6, s^2 = 9d^2 + 12m
            if m > 0:
                disc = 9 * d * d + 12 * m
                s = isqrt(disc)
                if s * s == disc and (s - 3 * d) % 6 == 0:
                    y = (s - 3 * d) // 6
                    if y >= 1:
                        return y + d, y
        d += 1
    return None


def main():
    n = int(sys.stdin.read().split()[0])
    r = solve(n)
    if r is None:
        print(-1)
    else:
        print(r[0], r[1])


if __name__ == "__main__":
    main()
