import sys
from itertools import combinations
from functools import reduce
from operator import xor
from math import comb


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    total = reduce(xor, a, 0)
    # K-subset XOR = total ^ (XOR of complement). Enumerate the smaller side.
    if k <= n - k:
        m = k
        flip = False
    else:
        m = n - k
        flip = True
    # C(n, m) <= C(n, k) <= 1e6
    best = 0
    if flip:
        for c in combinations(a, m):
            v = total ^ reduce(xor, c, 0)
            if v > best:
                best = v
    else:
        for c in combinations(a, m):
            v = reduce(xor, c, 0)
            if v > best:
                best = v
    print(best)


main()
