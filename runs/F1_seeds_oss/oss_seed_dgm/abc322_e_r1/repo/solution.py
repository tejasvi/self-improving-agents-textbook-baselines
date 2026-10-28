# Solution for "Product Development"
# DP over parameter values (capped at P) using multi-dimensional state compression.
# Constraints: N <= 100, K,P <= 5, so total states (P+1)^K <= 6^5 = 7776.
# For each development plan we consider adding it to existing states.
# The minimal total cost achieving all parameters >= P is output, or -1 if impossible.

import sys

def solve() -> None:
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
    total_states = base ** K
    INF = 10 ** 30
    dp = [INF] * total_states
    dp[0] = 0  # all zeros

    # pre‑compute powers for encoding/decoding
    pow_base = [base ** i for i in range(K)]

    for cost, adds in plans:
        new_dp = dp[:]  # copy for 0‑1 choice (cannot reuse plan)
        for idx in range(total_states):
            cur_cost = dp[idx]
            if cur_cost == INF:
                continue
            # decode idx to vector
            remaining = idx
            new_idx = 0
            for i in range(K):
                val = remaining % base
                remaining //= base
                nv = val + adds[i]
                if nv > P:
                    nv = P
                new_idx += nv * pow_base[i]
            # update
            if new_dp[new_idx] > cur_cost + cost:
                new_dp[new_idx] = cur_cost + cost
        dp = new_dp

    goal_idx = total_states - 1  # all coordinates = P
    ans = dp[goal_idx]
    if ans == INF:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
