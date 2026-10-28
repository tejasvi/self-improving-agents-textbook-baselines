import sys
from math import isqrt


def solve(N):
    # x = y + d, d >= 1, y >= 1:  3*d*y^2 + 3*d^2*y + d^3 = N
    d = 1
    while d * d * d + 3 * d * d + 3 * d <= N:
        # 3d y^2 + 3d^2 y + (d^3 - N) = 0
        D = 12 * d * N - 3 * d ** 4
        if D >= 0:
            s = isqrt(D)
            base = (s - 3 * d * d) // (6 * d)
            for y in (base - 1, base, base + 1, base + 2):
                if y >= 1 and (y + d) ** 3 - y ** 3 == N:
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
