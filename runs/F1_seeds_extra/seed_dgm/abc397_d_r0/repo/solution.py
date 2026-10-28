import sys
from math import isqrt


def solve(N):
    # x = y + d, N = d * (3y^2 + 3dy + d^2), and d^3 < N so d < cbrt(N) <= 1e6
    d = 1
    while d * d * d < N:
        if N % d == 0:
            k = N // d
            disc = 12 * k - 3 * d * d
            if disc > 0:
                s = isqrt(disc)
                if s * s == disc and (s - 3 * d) % 6 == 0:
                    y = (s - 3 * d) // 6
                    if y >= 1:
                        x = y + d
                        if x ** 3 - y ** 3 == N:
                            return x, y
        d += 1
    return None


def main():
    N = int(sys.stdin.read().split()[0])
    res = solve(N)
    if res is None:
        print(-1)
    else:
        print(res[0], res[1])


if __name__ == "__main__":
    main()
