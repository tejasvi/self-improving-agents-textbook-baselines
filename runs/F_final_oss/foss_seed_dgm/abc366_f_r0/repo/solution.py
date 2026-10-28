# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    funcs = []
    for _ in range(N):
        A = int(next(it))
        B = int(next(it))
        funcs.append((A, B))
    # Sort by descending A, then ascending B
    funcs.sort(key=lambda x: (-x[0], x[1]))
    # dp[t] = max value after selecting t functions
    NEG = -10**30  # sufficiently small
    dp = [NEG] * (K + 1)
    dp[0] = 1  # start value
    for A, B in funcs:
        # iterate t descending to avoid reuse
        for t in range(K - 1, -1, -1):
            if dp[t] != NEG:
                cand = A * dp[t] + B
                if cand > dp[t + 1]:
                    dp[t + 1] = cand
    print(dp[K])

if __name__ == "__main__":
    solve()
