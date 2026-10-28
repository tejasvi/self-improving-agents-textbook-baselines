# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    # Initialize dp arrays for each vitamin type (1-indexed types)
    dp = [[-1] * (X + 1) for _ in range(4)]  # dp[1], dp[2], dp[3]
    for t in (1, 2, 3):
        dp[t][0] = 0
    total = [0, 0, 0, 0]
    items_by_type = {1: [], 2: [], 3: []}
    for _ in range(N):
        V = int(next(it))
        A = int(next(it))
        C = int(next(it))
        items_by_type[V].append((A, C))
        total[V] += A
    # 0-1 knapsack for each vitamin type separately
    for typ in (1, 2, 3):
        cur = dp[typ]
        for A, C in items_by_type[typ]:
            # iterate backwards to avoid reuse
            for c in range(X, C - 1, -1):
                if cur[c - C] != -1:
                    val = cur[c - C] + A
                    if val > cur[c]:
                        cur[c] = val
    # Helper to check feasibility for a target T
    def feasible(T: int) -> bool:
        needed = 0
        for typ in (1, 2, 3):
            cur = dp[typ]
            min_cost = X + 1
            for c in range(X + 1):
                if cur[c] >= T:
                    min_cost = c
                    break
            if min_cost == X + 1:
                return False
            needed += min_cost
            if needed > X:
                return False
        return needed <= X

    # Upper bound for answer: limited by total amount of each vitamin
    high = min(total[1], total[2], total[3])
    low = 0
    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid - 1
    print(low)

if __name__ == "__main__":
    solve()
