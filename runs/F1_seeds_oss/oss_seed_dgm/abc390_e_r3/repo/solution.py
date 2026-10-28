# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    import sys
    N_X = sys.stdin.readline().split()
    if not N_X:
        return
    N, X = map(int, N_X)
    groups = {1: [], 2: [], 3: []}
    total_vit = {1: 0, 2: 0, 3: 0}
    for _ in range(N):
        line = sys.stdin.readline().split()
        if not line:
            continue
        v, a, c = map(int, line)
        groups[v].append((c, a))  # weight, value
        total_vit[v] += a
    # Upper bound for answer is the minimal total across vitamins
    max_possible = min(total_vit[1], total_vit[2], total_vit[3])

    # Compute DP for each vitamin type: dp[g][cal] = max amount attainable with at most cal calories
    dp = {}
    for vt in (1, 2, 3):
        dp_arr = [-10**18] * (X + 1)
        dp_arr[0] = 0
        for w, val in groups[vt]:
            # 0/1 knapsack, iterate backwards
            for cal in range(X, w - 1, -1):
                prev = dp_arr[cal - w] + val
                if prev > dp_arr[cal]:
                    dp_arr[cal] = prev
        # make it non-decreasing so dp_arr[cal] = max attainable with <= cal calories
        for cal in range(1, X + 1):
            if dp_arr[cal - 1] > dp_arr[cal]:
                dp_arr[cal] = dp_arr[cal - 1]
        dp[vt] = dp_arr

    # Helper to check feasibility for target T
    def feasible(T: int) -> bool:
        total_needed = 0
        for vt in (1, 2, 3):
            arr = dp[vt]
            # find minimal calories where amount >= T, using linear scan (X <= 5000)
            cal_needed = None
            for cal in range(X + 1):
                if arr[cal] >= T:
                    cal_needed = cal
                    break
            if cal_needed is None:
                return False
            total_needed += cal_needed
            if total_needed > X:  # early exit
                return False
        return total_needed <= X

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
