# Write your solution here. Read from stdin, write to stdout.
import sys
from functools import cmp_to_key

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
    # Comparator: f before g if B_f/(A_f-1) >= B_g/(A_g-1)
    # Treat A==1 as having infinite ratio, thus placed first.
    def cmp(item1, item2):
        A1, B1 = item1
        A2, B2 = item2
        if A1 == 1 and A2 == 1:
            return 0
        if A1 == 1:
            return -1  # item1 (A=1) should come before
        if A2 == 1:
            return 1   # item2 (A=1) should come before item1
        # compare B1/(A1-1) and B2/(A2-1) in decreasing order
        left = B1 * (A2 - 1)
        right = B2 * (A1 - 1)
        if left > right:
            return -1  # item1 has larger ratio, comes first
        if left < right:
            return 1   # item2 has larger ratio
        return 0
    funcs.sort(key=cmp_to_key(cmp))
    INF_NEG = -10**30
    dp = [INF_NEG] * (K + 1)
    dp[0] = 1  # start value
    for A, B in funcs:
        for t in range(K, 0, -1):
            if dp[t-1] != INF_NEG:
                val = A * dp[t-1] + B
                if val > dp[t]:
                    dp[t] = val
    print(dp[K])

if __name__ == "__main__":
    solve()
