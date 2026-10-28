# Write your solution here. Read from stdin, write to stdout.

import sys

def feasible(H, N, X, U, D):
    # interval for first tooth
    low = max(0, H - D[0])
    high = min(U[0], H)
    if low > high:
        return False
    cur_low, cur_high = low, high
    for i in range(1, N):
        low = max(0, H - D[i])
        high = min(U[i], H)
        if low > high:
            return False
        # expand previous interval by X
        cur_low = max(low, cur_low - X)
        cur_high = min(high, cur_high + X)
        if cur_low > cur_high:
            return False
    return True

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    U = []
    D = []
    sumU = 0
    sumD = 0
    min_sum = 10**20
    for _ in range(N):
        u = int(next(it))
        d = int(next(it))
        U.append(u)
        D.append(d)
        sumU += u
        sumD += d
        s = u + d
        if s < min_sum:
            min_sum = s
    lo = 0
    hi = min_sum  # inclusive upper bound
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid, N, X, U, D):
            lo = mid
        else:
            hi = mid - 1
    H = lo
    ans = sumU + sumD - N * H
    print(ans)

if __name__ == "__main__":
    solve()
