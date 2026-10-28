# solution.py
import sys

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    funcs = []
    for _ in range(N):
        a = int(next(it))
        b = int(next(it))
        funcs.append((a, b))
    # Sorting: functions with a==1 should be innermost, so they come first.
    # For a!=1, optimal order (inner to outer) is decreasing b/(a-1).
    def sort_key(ab):
        a, b = ab
        if a == 1:
            return float('-inf')  # ensure these come first (inner)
        return -b / (a - 1)       # larger b/(a-1) first
    funcs.sort(key=sort_key)
    NEG = -10**30
    dp = [NEG] * (K + 1)
    dp[0] = 1
    for a, b in funcs:
        for t in range(K, 0, -1):
            val = a * dp[t - 1] + b
            if val > dp[t]:
                dp[t] = val
    print(dp[K])

if __name__ == "__main__":
    solve()
