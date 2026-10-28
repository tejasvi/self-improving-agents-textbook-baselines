import sys
from itertools import combinations
from functools import reduce
from operator import xor


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    k = int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    total = reduce(xor, a, 0)
    # XOR of a K-subset = total ^ XOR of its complement (size N-K).
    # Enumerate the smaller side: m = min(K, N-K) <= N/2, so C(N,m) <= 1e6.
    if k > n - k:
        m = n - k
        best = max(total ^ reduce(xor, c, 0) for c in combinations(a, m))
    else:
        m = k
        best = max(reduce(xor, c, 0) for c in combinations(a, m))
    print(best)


main()
