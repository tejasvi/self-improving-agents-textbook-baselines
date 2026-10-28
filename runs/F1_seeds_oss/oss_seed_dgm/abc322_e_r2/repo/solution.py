# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    import sys
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
    # DP over states, each dimension capped at P
    base = P + 1
    # multipliers for encoding
    mul = [1]
    for i in range(1, K):
        mul.append(mul[-1] * base)
    total_states = base ** K
    INF = 10**30
    dp = [INF] * total_states
    dp[0] = 0
    def encode(vec):
        idx = 0
        for j in range(K):
            idx += vec[j] * mul[j]
        return idx
    goal_vec = [P] * K
    goal_idx = encode(goal_vec)
    for cost, add in plans:
        new_dp = dp[:]  # 0/1 knapsack transition
        for idx in range(total_states):
            cur = dp[idx]
            if cur == INF:
                continue
            # decode idx
            tmp = idx
            cur_vec = [0] * K
            for j in range(K):
                cur_vec[j] = tmp % base
                tmp //= base
            # apply plan
            nxt_vec = [0] * K
            for j in range(K):
                v = cur_vec[j] + add[j]
                if v > P:
                    v = P
                nxt_vec[j] = v
            nxt_idx = encode(nxt_vec)
            if new_dp[nxt_idx] > cur + cost:
                new_dp[nxt_idx] = cur + cost
        dp = new_dp
    ans = dp[goal_idx]
    print(ans if ans != INF else -1)

if __name__ == "__main__":
    solve()
