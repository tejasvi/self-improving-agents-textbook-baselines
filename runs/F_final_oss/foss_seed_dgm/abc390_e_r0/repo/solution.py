# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    # Separate items by vitamin type
    groups = {1: [], 2: [], 3: []}
    for _ in range(N):
        v = int(next(it))
        a = int(next(it))
        c = int(next(it))
        groups[v].append((c, a))  # (calories, amount)

    # For each vitamin group, compute dp[c] = max amount achievable with total calories exactly c
    # Initialize with -1 (impossible), dp[0] = 0
    def compute_best(group_items):
        dp = [-1] * (X + 1)
        dp[0] = 0
        for cal, amt in group_items:
            # 0/1 knapsack, iterate backwards
            for cur in range(X, cal - 1, -1):
                if dp[cur - cal] != -1:
                    cand = dp[cur - cal] + amt
                    if cand > dp[cur]:
                        dp[cur] = cand
        # Convert to prefix maximum: best[c] = max amount reachable with calories up to c
        best = [-1] * (X + 1)
        cur_max = -1
        for c in range(X + 1):
            if dp[c] > cur_max:
                cur_max = dp[c]
            best[c] = cur_max
        return best

    best1 = compute_best(groups[1])
    best2 = compute_best(groups[2])
    best3 = compute_best(groups[3])

    ans = 0
    # Enumerate calories used for vitamin 1 and 2, remaining goes to vitamin 3 (or unused)
    for c1 in range(X + 1):
        if best1[c1] < 0:
            continue
        rem_after_c1 = X - c1
        for c2 in range(rem_after_c1 + 1):
            if best2[c2] < 0:
                continue
            c3 = rem_after_c1 - c2
            if best3[c3] < 0:
                continue
            cur = min(best1[c1], best2[c2], best3[c3])
            if cur > ans:
                ans = cur
    print(ans)

if __name__ == "__main__":
    solve()
