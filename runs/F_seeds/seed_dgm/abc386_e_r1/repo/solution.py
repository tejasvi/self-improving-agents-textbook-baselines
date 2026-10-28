import sys
from itertools import combinations


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]

    # XOR of K elements = total ^ (XOR of the N-K unchosen elements).
    # Enumerate the smaller side m; C(N,m) == C(N,K) <= 1e6.
    if k <= n - k:
        m = k
        base = 0
    else:
        m = n - k
        total = 0
        for v in a:
            total ^= v
        base = total

    best = -1
    if m == 0:
        best = base
    else:
        for comb in combinations(a, m):
            x = 0
            for v in comb:
                x ^= v
            y = x ^ base
            if y > best:
                best = y
    print(best)


main()
