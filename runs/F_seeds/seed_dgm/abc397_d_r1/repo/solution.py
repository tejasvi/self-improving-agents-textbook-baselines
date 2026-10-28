import sys
from math import isqrt


def solve(N):
    # x - y = d, N = d * (3y^2 + 3dy + d^2), y >= 1 implies d^3 < N.
    d = 1
    while d * d * d < N:
        if N % d == 0:
            m = N // d
            D = 12 * m - 3 * d * d
            if D > 0:
                s = isqrt(D)
                if s * s == D and (s - 3 * d) > 0 and (s - 3 * d) % 6 == 0:
                    y = (s - 3 * d) // 6
                    x = y + d
                    if y >= 1 and x ** 3 - y ** 3 == N:
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
