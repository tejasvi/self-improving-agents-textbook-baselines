import sys
from math import isqrt


def solve(n):
    # x - y = a, N = a * (3y^2 + 3ay + a^2), and a^3 <= N so a <= 1e6.
    a = 1
    while a * a * a <= n:
        if n % a == 0:
            b = n // a
            D = 12 * b - 3 * a * a
            if D > 0:
                s = isqrt(D)
                if s * s == D and s > 3 * a and (s - 3 * a) % 6 == 0:
                    y = (s - 3 * a) // 6
                    if y >= 1:
                        x = y + a
                        if x ** 3 - y ** 3 == n:
                            return x, y
        a += 1
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
