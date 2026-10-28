# Solution for Maximize XOR problem
import sys
import itertools

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    max_xor = 0
    # Enumerate all combinations of K indices
    # Since C(N, K) <= 10^6, this is feasible.
    for combo in itertools.combinations(A, K):
        x = 0
        for v in combo:
            x ^= v
        if x > max_xor:
            max_xor = x
    sys.stdout.write(str(max_xor))

if __name__ == "__main__":
    solve()
