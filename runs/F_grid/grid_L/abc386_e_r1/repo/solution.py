import sys
from itertools import combinations


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = [int(x) for x in data[2:2 + n]]

    # XOR of a K-subset S equals (XOR of all) ^ (XOR of complement),
    # so we may enumerate the smaller of the two sides.
    base = 0
    if k <= n - k:
        m = k
    else:
        m = n - k
        for v in a:
            base ^= v

    if m == 0:
        print(base)
        return

    best = 0
    if m == 1:
        for v in a:
            x = v ^ base
            if x > best:
                best = x
    else:
        for combo in combinations(a, m):
            x = base
            for v in combo:
                x ^= v
            if x > best:
                best = x
    print(best)


main()
