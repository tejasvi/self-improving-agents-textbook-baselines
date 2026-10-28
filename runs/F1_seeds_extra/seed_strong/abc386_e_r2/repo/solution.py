import sys
from itertools import combinations
from functools import reduce
from operator import xor


def main():
    data = sys.stdin.buffer.read().split()
    n, k = int(data[0]), int(data[1])
    a = [int(x) for x in data[2:2 + n]]
    total = reduce(xor, a, 0)
    # XOR of K-subset = total ^ XOR of complement (size N-K).
    # Enumerate the smaller side; fix the target accordingly.
    if k <= n - k:
        vals = {reduce(xor, c, 0) for c in combinations(a, k)}
        ans = max(vals)
    else:
        m = n - k
        vals = {reduce(xor, c, 0) for c in combinations(a, m)}
        ans = max(total ^ x for x in vals)
    print(ans)


main()
