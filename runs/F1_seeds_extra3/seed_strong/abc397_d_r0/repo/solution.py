import sys
from math import isqrt


def solve(n):
    # x = y + d, n = d * (3y^2 + 3dy + d^2), y >= 1
    d = 1
    while d * (d * d + 3 * d + 3) <= n:
        if n % d == 0:
            m = n // d
            disc = 12 * m - 3 * d * d
            s = isqrt(disc)
            if s * s == disc and (s - 3 * d) % 6 == 0:
                y = (s - 3 * d) // 6
                if y >= 1:
                    x = y + d
                    if x ** 3 - y ** 3 == n:
                        return x, y
        d += 1
    return None


def main():
    n = int(sys.stdin.read().split()[0])
    res = solve(n)
    if res is None:
        print(-1)
    else:
        print(res[0], res[1])


if __name__ == "__main__":
    main()
