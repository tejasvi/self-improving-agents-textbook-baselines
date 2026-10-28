import sys
from math import isqrt


def solve(N):
    d = 1
    while d * d * d < N:
        if N % d == 0:
            M = N // d
            T = 12 * M - 3 * d * d
            if T > 0:
                S = isqrt(T)
                if S * S == T and S > 3 * d and (S - 3 * d) % 6 == 0:
                    y = (S - 3 * d) // 6
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
