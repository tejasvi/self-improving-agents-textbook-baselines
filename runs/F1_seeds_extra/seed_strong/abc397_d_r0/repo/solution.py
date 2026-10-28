import sys
from math import isqrt


def solve(N):
    d = 1
    # N = d*(3y^2 + 3dy + d^2) with y >= 1 implies d*(d^2+3d+3) <= N
    while d * (d * d + 3 * d + 3) <= N:
        if N % d == 0:
            M = N // d
            D = 12 * M - 3 * d * d
            if D > 0:
                s = isqrt(D)
                if s * s == D and (s - 3 * d) % 6 == 0:
                    y = (s - 3 * d) // 6
                    if y >= 1:
                        return (y + d, y)
        d += 1
    return None


def main():
    N = int(sys.stdin.read().split()[0])
    r = solve(N)
    if r is None:
        print(-1)
    else:
        print(r[0], r[1])


if __name__ == "__main__":
    main()
