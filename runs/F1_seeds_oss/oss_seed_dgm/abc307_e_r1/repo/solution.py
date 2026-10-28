# Distinct Adjacent problem solution
# Counts colorings of a cycle with N vertices and M colors, such that adjacent vertices have distinct colors.
# The formula is: (M-1)^N + (-1)^N * (M-1) (mod 998244353)

import sys

MOD = 998244353

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    # Since M >= 2 per constraints, M-1 is non‑negative.
    pow_term = pow(M - 1, N, MOD)
    sign = 1 if N % 2 == 0 else -1
    ans = (pow_term + sign * (M - 1)) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
