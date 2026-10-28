from math import isqrt


def solve(n):
    d = 1
    while d * d * d < n:
        if n % d == 0:
            q = n // d
            D = 12 * q - 3 * d * d
            if D > 0:
                s = isqrt(D)
                if s * s == D and (s - 3 * d) > 0 and (s - 3 * d) % 6 == 0:
                    y = (s - 3 * d) // 6
                    x = y + d
                    if y >= 1 and x ** 3 - y ** 3 == n:
                        return x, y
        d += 1
    return None


def main():
    n = int(input())
    res = solve(n)
    if res is None:
        print(-1)
    else:
        print(res[0], res[1])


if __name__ == "__main__":
    main()
