import sys
import math

def find_pair(N: int):
    # Upper bound for d = x - y. Since N = d * (x^2 + xy + y^2) and the second factor is > d^2,
    # we have N > d^3, therefore d < N^{1/3}. We iterate up to cube root + a small margin.
    max_d = int(round(N ** (1/3))) + 2
    for d in range(1, max_d + 1):
        if N % d != 0:
            continue
        M = N // d  # M = x^2 + xy + y^2
        # Discriminant of 3y^2 + 3dy + d^2 - M = 0
        delta = 12 * M - 3 * d * d
        if delta <= 0:
            continue
        s = math.isqrt(delta)
        if s * s != delta:
            continue
        # y = ( -3d + s ) / 6  must be positive integer
        if (s - 3 * d) % 6 != 0:
            continue
        y = (s - 3 * d) // 6
        if y <= 0:
            continue
        x = y + d
        # Verify (optional, safe guard)
        if x ** 3 - y ** 3 == N:
            return x, y
    return None

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    res = find_pair(N)
    if res is None:
        print(-1)
    else:
        print(res[0], res[1])

if __name__ == "__main__":
    main()
