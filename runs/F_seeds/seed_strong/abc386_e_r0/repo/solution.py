import sys
from itertools import combinations
from functools import reduce
from operator import xor


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    best = 0
    if k == 0:
        print(0)
        return
    # Enumerate all K-subsets (count <= 1e6 by constraint).
    # Use the XOR of the complement trick is unnecessary; direct enumeration suffices.
    for c in combinations(a, k):
        x = reduce(xor, c)
        if x > best:
            best = x
    print(best)


main()
