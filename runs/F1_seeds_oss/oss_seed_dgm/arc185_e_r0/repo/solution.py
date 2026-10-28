# Write your solution here. Read from stdin, write to stdout.

import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    A = [int(next(it)) for _ in range(n)]
    max_a = max(A)
    # precompute phi up to max_a
    phi = list(range(max_a + 1))
    for i in range(2, max_a + 1):
        if phi[i] == i:  # prime
            for j in range(i, max_a + 1, i):
                phi[j] -= phi[j] // i
    # precompute divisors for each number up to max_a
    divisors = [[] for _ in range(max_a + 1)]
    for d in range(1, max_a + 1):
        for multiple in range(d, max_a + 1, d):
            divisors[multiple].append(d)
    # g[d] = sum_{i: d divides A_i} 2^{i-1} (mod MOD)
    g = [0] * (max_a + 1)
    ans = 0  # dp for previous prefix
    cur_pow = 1  # 2^{i-1} for current i (starts with i=1)
    out_lines = []
    for idx, x in enumerate(A, start=1):
        # contribution from pairs (i, idx) where i < idx
        contrib = 0
        for d in divisors[x]:
            contrib = (contrib + g[d] * phi[d]) % MOD
        ans = (ans * 2 + contrib) % MOD
        out_lines.append(str(ans))
        # update g for future contributions
        for d in divisors[x]:
            g[d] = (g[d] + cur_pow) % MOD
        cur_pow = (cur_pow * 2) % MOD
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
