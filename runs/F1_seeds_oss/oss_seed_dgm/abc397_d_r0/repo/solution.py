# Write your solution here. Read from stdin, write to stdout.
import sys
import math

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    # Upper bound for d = x - y is cube root of N
    # Compute integer cube root safely
    max_d = int(round(N ** (1/3))) + 2
    # Ensure max_d not too small due to rounding issues
    while (max_d+1)**3 <= N:
        max_d += 1
    while max_d**3 > N:
        max_d -= 1
    for d in range(1, max_d + 1):
        if N % d != 0:
            continue
        M = N // d
        # discriminant of quadratic 3y^2 + 3dy + (d^2 - M) = 0
        delta = 12 * M - 3 * d * d
        if delta < 0:
            continue
        s = math.isqrt(delta)
        if s * s != delta:
            continue
        # y = (s - 3d) / 6 must be integer and positive
        if (s - 3 * d) % 6 != 0:
            continue
        y = (s - 3 * d) // 6
        if y <= 0:
            continue
        x = y + d
        if x**3 - y**3 == N:
            print(x, y)
            return
    print(-1)

if __name__ == "__main__":
    main()
