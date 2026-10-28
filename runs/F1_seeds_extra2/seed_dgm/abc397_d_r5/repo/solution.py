import sys
from math import isqrt


def solve(n):
    a = 1
    while a * a * a <= n:
        if n % a == 0:
            b = n // a
            t = 4 * b - a * a
            if t > 0 and t % 3 == 0:
                s2 = t // 3
                s = isqrt(s2)
                if s * s == s2 and s > a and (s - a) % 2 == 0:
                    y = (s - a) // 2
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
