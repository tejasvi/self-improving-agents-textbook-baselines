# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    MOD = 998244353
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    # Compute (M-1)^N modulo MOD
    base = (M - 1) % MOD
    pow_val = pow(base, N, MOD)
    # term = (-1)^N * (M-1)
    if N % 2 == 0:
        term = base
    else:
        term = (-base) % MOD
    ans = (pow_val + term) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
