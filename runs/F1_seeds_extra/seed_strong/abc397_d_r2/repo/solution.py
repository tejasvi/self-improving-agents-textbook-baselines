import sys
from math import isqrt

def solve(N):
    # x^3 - y^3 = (x-y)(x^2+xy+y^2). Let d = x-y >= 1, then
    # N = d * (3y^2 + 3dy + d^2), so M = N/d and 3y^2+3dy+(d^2-M)=0.
    d = 1
    while d * d * d < N:
        if N % d == 0:
            M = N // d
            disc = 12 * M - 3 * d * d
            if disc > 0:
                r = isqrt(disc)
                if r * r == disc and (r - 3 * d) % 6 == 0:
                    y = (r - 3 * d) // 6
                    if y >= 1:
                        x = y + d
                        if x ** 3 - y ** 3 == N:
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
