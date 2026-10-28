import sys
from itertools import combinations
from functools import reduce
from operator import xor


def main():
    data = sys.stdin.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    total = reduce(xor, a, 0)
    # XOR of a K-subset S = total ^ XOR(complement of S). Enumerate the smaller
    # side m = min(K, N-K); the max is over (XOR of m-subset) ^ offset.
    m = k
    offset = 0
    if k > n - k:
        m = n - k
        offset = total
    if m == 0:
        print(offset)
        return
    best = -1
    for c in combinations(a, m):
        v = reduce(xor, c) ^ offset
        if v > best:
            best = v
    print(best)


main()
