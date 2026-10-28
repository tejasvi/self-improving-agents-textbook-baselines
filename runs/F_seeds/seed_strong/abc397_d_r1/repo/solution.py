import sys
from math import isqrt

def solve(N):
    # x^3 - y^3 = (x-y)(x^2+xy+y^2). Let d = x - y >= 1, M = N / d.
    # Then M = 3y^2 + 3dy + d^2, so 12M - 3d^2 = (6y+3d)^2 must be a perfect square s^2
    # with s = 6y + 3d, i.e. s > 3d and s % 6 == 3d % 6.
    d = 1
    while d * d * d < N:
        if N % d == 0:
            M = N // d
            t = 12 * M - 3 * d * d
            if t > 0:
                s = isqrt(t)
                if s * s == t and s > 3 * d and (s - 3 * d) % 6 == 0:
                    y = (s - 3 * d) // 6
                    if y >= 1:
                        return (y + d, y)
        d += 1
    return None

def main():
    N = int(sys.stdin.readline())
    r = solve(N)
    if r is None:
        print(-1)
    else:
        print(r[0], r[1])

if __name__ == "__main__":
    main()
