import sys
from math import isqrt


def solve(n):
    # x^3 - y^3 = (x-y)(x^2+xy+y^2). Let a = x-y >= 1, x = y+a.
    # Then n = a*(3y^2 + 3ay + a^2). Since y>=1, n > a^3, so a < n^(1/3).
    a = 1
    while a * a * a < n:
        if n % a == 0:
            q = n // a
            # 3y^2 + 3a y + (a^2 - q) = 0  ->  y = (-3a + sqrt(12q - 3a^2)) / 6
            d = 12 * q - 3 * a * a
            if d > 0:
                s = isqrt(d)
                if s * s == d and (s - 3 * a) > 0 and (s - 3 * a) % 6 == 0:
                    y = (s - 3 * a) // 6
                    x = y + a
                    if x > 0 and y > 0 and x ** 3 - y ** 3 == n:
                        return x, y
        a += 1
    return None


def main():
    n = int(sys.stdin.read().split()[0])
    r = solve(n)
    if r is None:
        print(-1)
    else:
        print(r[0], r[1])


if __name__ == "__main__":
    main()
