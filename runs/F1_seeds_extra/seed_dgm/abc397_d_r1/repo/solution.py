import sys
from math import isqrt


def solve(N):
    # x = y + d, N = d * (3y^2 + 3dy + d^2); d^3 <= N so d <= 10^6
    d = 1
    while d * d * d <= N:
        if N % d == 0:
            M = N // d
            D = 12 * M - 3 * d * d
            if D >= 0:
                r = isqrt(D)
                if r * r == D and (r - 3 * d) >= 0 and (r - 3 * d) % 6 == 0:
                    y = (r - 3 * d) // 6
                    if y >= 1:
                        return (y + d, y)
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
