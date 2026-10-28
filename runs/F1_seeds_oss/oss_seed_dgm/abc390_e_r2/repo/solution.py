# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    items = {1: [], 2: [], 3: []}
    for _ in range(N):
        v = int(next(it))
        a = int(next(it))
        c = int(next(it))
        items[v].append((c, a))  # (cost, amount)
    # DP for each vitamin type: max amount achievable with exactly calories c (0..X)
    dps = {}
    for vt in (1, 2, 3):
        dp = [-1] * (X + 1)
        dp[0] = 0
        for cost, amt in items[vt]:
            # 0/1 knapsack over calories
            for cal in range(X, cost - 1, -1):
                if dp[cal - cost] != -1:
                    val = dp[cal - cost] + amt
                    if val > dp[cal]:
                        dp[cal] = val
        dps[vt] = dp
    # Upper bound for answer: minimum of the maximum amount each type can reach with at most X calories
    max_possible = min(max(dps[1]), max(dps[2]), max(dps[3]))
    if max_possible < 0:
        max_possible = 0
    INF = X + 1
    # Helper to check feasibility of achieving at least m of each vitamin within X calories
    def feasible(m: int) -> bool:
        total = 0
        for vt in (1, 2, 3):
            dp = dps[vt]
            need = INF
            for cal in range(X + 1):
                if dp[cal] >= m:
                    need = cal
                    break
            if need == INF:
                return False
            total += need
            if total > X:
                return False
        return total <= X
    lo, hi = 0, max_possible
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()
