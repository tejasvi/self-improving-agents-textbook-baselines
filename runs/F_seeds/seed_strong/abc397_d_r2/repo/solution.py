import sys
from math import isqrt

def main():
    N = int(sys.stdin.read().split()[0])
    d = 1
    while d * d * d <= N:
        if N % d == 0:
            s = N // d  # s = 3y^2 + 3yd + d^2
            D = 12 * s - 3 * d * d
            if D >= 0:
                r = isqrt(D)
                if r * r == D and (r - 3 * d) >= 0 and (r - 3 * d) % 6 == 0:
                    y = (r - 3 * d) // 6
                    if y >= 1:
                        print(y + d, y)
                        return
        d += 1
    print(-1)

main()
