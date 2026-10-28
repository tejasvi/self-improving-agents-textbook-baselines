import sys
from math import isqrt


def solve(n):
    d = 1
    while d * d * d < n:
        if n % d == 0:
            m = n // d
            disc = 12 * m - 3 * d * d
            if disc >= 0:
                r = isqrt(disc)
                if r * r == disc and r > 3 * d and (r - 3 * d) % 6 == 0:
                    y = (r - 3 * d) // 6
                    if y > 0:
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
