# Solution for Maximize XOR problem
# We are given N (up to 2e5) numbers and an integer K such that C(N, K) <= 10^6.
# The constraint guarantees that the total number of K‑element subsets is at most one million,
# therefore a direct enumeration of all subsets is feasible.
# The algorithm simply enumerates every combination of K elements, computes its XOR and keeps the maximum.
# The time complexity is O(C(N, K) * K) which is acceptable under the given bound.
# Memory usage is O(1) besides the input array.

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

    # If K == 0 (not possible per constraints) the XOR would be 0.
    # For safety we handle it.
    if K == 0:
        print(0)
        return

    max_xor = 0
    # Enumerate all K‑element subsets.
    for combo in combinations(A, K):
        xor_val = 0
        for v in combo:
            xor_val ^= v
        if xor_val > max_xor:
            max_xor = xor_val
    print(max_xor)

if __name__ == "__main__":
    solve()
