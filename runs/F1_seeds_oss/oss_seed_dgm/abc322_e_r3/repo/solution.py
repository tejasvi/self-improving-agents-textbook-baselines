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
    total_states = base ** K
    INF = 10**18
    dp = [INF] * total_states
    dp[0] = 0  # all zeros
    # helper to encode list of values to index
    def encode(vals):
        idx = 0
        mul = 1
        for v in vals:
            idx += v * mul
            mul *= base
        return idx
    # decode is needed during transition
    def decode(idx):
        vals = []
        for _ in range(K):
            vals.append(idx % base)
            idx //= base
        return vals
    for cost, adds in plans:
        dp_next = dp[:]  # copy for 0/1 knap
        for state_idx in range(total_states):
            cur = dp[state_idx]
            if cur == INF:
                continue
            # decode current state
            cur_vals = []
            tmp = state_idx
            for _ in range(K):
                cur_vals.append(tmp % base)
                tmp //= base
            # compute new values capped at P
            new_vals = []
            for j in range(K):
                nv = cur_vals[j] + adds[j]
                if nv > P:
                    nv = P
                new_vals.append(nv)
            new_idx = 0
            mul = 1
            for v in new_vals:
                new_idx += v * mul
                mul *= base
            if dp_next[new_idx] > cur + cost:
                dp_next[new_idx] = cur + cost
        dp = dp_next
    goal_idx = (P) * (base ** 0)  # all components are P -> compute encode directly
    # but need encode of [P]*K
    goal_idx = encode([P] * K)
    ans = dp[goal_idx]
    if ans >= INF:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
