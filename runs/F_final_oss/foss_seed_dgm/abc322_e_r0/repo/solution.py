# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    P = int(next(it))
    plans = []
    for _ in range(N):
        C = int(next(it))
        A = [int(next(it)) for _ in range(K)]
        plans.append((C, A))
    base = P + 1
    size = base ** K
    INF = 10**18
    dp = [INF] * size
    dp[0] = 0
    # precompute power multipliers for encoding
    mult = [base ** i for i in range(K)]
    for C, A in plans:
        ndp = dp[:]  # copy current dp for transitions
        for idx in range(size):
            cur_cost = dp[idx]
            if cur_cost == INF:
                continue
            # decode idx into vector of current parameter values
            tmp = idx
            vals = []
            for _ in range(K):
                vals.append(tmp % base)
                tmp //= base
            # compute new values after applying this plan
            new_vals = [min(P, vals[j] + A[j]) for j in range(K)]
            # encode new_vals back to index
            new_idx = 0
            for j in range(K):
                new_idx += new_vals[j] * mult[j]
            if ndp[new_idx] > cur_cost + C:
                ndp[new_idx] = cur_cost + C
        dp = ndp
    # target index where each parameter is at least P (capped to P)
    target_idx = 0
    for j in range(K):
        target_idx += P * mult[j]
    ans = dp[target_idx]
    if ans == INF:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
