# Solution for Maximize XOR problem
# Reads input, enumerates all combinations of size K (or N-K if smaller) and computes maximum XOR.
# The constraint ensures that number of combinations is at most 1e6, making brute-force feasible.

import sys
from itertools import combinations

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # If K is larger than N-K, it is more efficient to iterate over the complement subsets.
    # For any subset S of size K, let C be its complement (size N-K).
    # Then xor(S) = xor_all ^ xor(C).
    # So maximizing xor(S) is equivalent to maximizing xor_all ^ xor(C) over subsets C of size N-K.
    # We will iterate over the smaller of K and N-K.
    if K > N - K:
        # iterate over complement size
        size = N - K
        xor_all = 0
        for v in A:
            xor_all ^= v
        max_xor = 0
        # iterate all subsets of size 'size'
        for subset in combinations(A, size):
            cur = 0
            for v in subset:
                cur ^= v
            # xor of the K-chosen elements = xor_all ^ cur
            candidate = xor_all ^ cur
            if candidate > max_xor:
                max_xor = candidate
        print(max_xor)
    else:
        size = K
        max_xor = 0
        for subset in combinations(A, size):
            cur = 0
            for v in subset:
                cur ^= v
            if cur > max_xor:
                max_xor = cur
        print(max_xor)

if __name__ == "__main__":
    solve()
