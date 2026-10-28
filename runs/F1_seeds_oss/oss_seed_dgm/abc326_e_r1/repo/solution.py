# Solution for "Revenge of The Salary of AtCoder Inc."
# Computes expected salary modulo 998244353.
# Expected value = (1/N) * sum_{i=1}^N A_i * ((N+1)/N)^{i-1}
# All operations are done modulo MOD = 998244353.

import sys

def solve() -> None:
    MOD = 998244353
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    invN = pow(N, MOD - 2, MOD)
    r = (N + 1) * invN % MOD  # (N+1)/N modulo MOD
    power = 1
    total = 0
    for a in A:
        total = (total + a * power) % MOD
        power = power * r % MOD
    ans = total * invN % MOD
    print(ans)

if __name__ == "__main__":
    solve()
