# Solution for "Revenge of The Salary of AtCoder Inc."
# Expected value of the total paid amount in the described random process.
# The recurrence:
#   E[i] = (1/N) * sum_{y=i+1..N} (A_y + E[y])
# where E[N] = 0 and answer is E[0].
# Compute from N down to 0 using suffix sums.

import sys

def solve() -> None:
    MOD = 998244353
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [0] * (N + 1)  # 1-indexed
    for i in range(1, N + 1):
        A[i] = int(next(it))
    invN = pow(N, MOD - 2, MOD)
    E = [0] * (N + 1)
    suffix = 0  # sum_{y=i+1..N} (A_y + E[y]) for current i
    for i in range(N, -1, -1):
        # E[i] computed from current suffix (which corresponds to i+1 .. N)
        E[i] = suffix * invN % MOD
        if i >= 1:
            suffix = (suffix + A[i] + E[i]) % MOD
    # Expected value modulo MOD is E[0]
    print(E[0])

if __name__ == "__main__":
    solve()
