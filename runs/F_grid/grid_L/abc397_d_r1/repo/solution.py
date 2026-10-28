import math


def solve(N):
    d = 1
    while d * d * d < N:
        if N % d == 0:
            M = N // d
            D = 12 * M - 3 * d * d
            if D > 0:
                s = math.isqrt(D)
                if s * s == D and (s - 3 * d) % 6 == 0:
                    y = (s - 3 * d) // 6
                    if y >= 1:
                        return y + d, y
        d += 1
    return None


def main():
    N = int(input())
    res = solve(N)
    if res is None:
        print(-1)
    else:
        print(res[0], res[1])


if __name__ == "__main__":
    main()
