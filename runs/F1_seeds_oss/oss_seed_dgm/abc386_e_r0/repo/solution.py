# Write your solution here. Read from stdin, write to stdout.

import sys
import itertools
import operator

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    # Since \binom{N}{K} <= 10^6, we can enumerate all combinations safely.
    max_xor = 0
    # Use local variables for speed
    xor_op = operator.xor
    for comb in itertools.combinations(A, K):
        cur = 0
        for v in comb:
            cur = xor_op(cur, v)
        if cur > max_xor:
            max_xor = cur
    sys.stdout.write(str(max_xor))

if __name__ == "__main__":
    solve()
