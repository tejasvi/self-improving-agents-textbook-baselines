import sys
from math import isqrt


def solve(N):
    # N = (x-y)(x^2+xy+y^2). With d = x-y >= 1, s = N/d:
    # s = 3y^2 + 3dy + d^2  =>  y = (-3d + sqrt(12s - 3d^2)) / 6
    # Since s >= d^2, d^3 <= N, so d <= 10^6.
    d = 1
    while d * d * d <= N:
        if N % d == 0:
            s = N // d
            D = 12 * s - 3 * d * d
            if D >= 0:
                r = isqrt(D)
                if r * r == D and (r - 3 * d) % 6 == 0:
                    y = (r - 3 * d) // 6
                    if y >= 1:
                        return y + d, y
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
