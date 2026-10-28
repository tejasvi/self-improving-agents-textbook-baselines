import sys
from itertools import combinations
from functools import reduce
from operator import xor


def main():
    data = sys.stdin.read().split()
    n, K = int(data[0]), int(data[1])
    A = [int(x) for x in data[2:2 + n]]
    total = reduce(xor, A, 0)
    # Choosing K elements S; XOR(S) = total ^ XOR(complement), complement has size N-K.
    # Enumerate the smaller side k = min(K, N-K) with C(n,k) = C(n,K) <= 1e6.
    # If K is the smaller side, target = 0 and we maximize XOR of k-subset.
    # Otherwise target = total and we maximize total ^ XOR of (N-K)-subset.
    k = min(K, n - K)
    target = 0 if K == k else total
    if k == 0:
        print(target)
        return
    if k == 1:
        print(max(target ^ a for a in A))
        return
    best = -1
    for pre in combinations(range(n), k - 1):
        p = target
        for i in pre:
            p ^= A[i]
        start = pre[-1] + 1
        if start < n:
            v = max(p ^ a for a in A[start:])
            if v > best:
                best = v
    print(best)


main()
