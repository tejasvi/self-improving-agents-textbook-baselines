# Write your solution here. Read from stdin, write to stdout.
import sys

def feasible(H, U, D, X):
    n = len(U)
    # interval for first tooth
    low = max(0, H - D[0])
    high = min(U[0], H)
    if low > high:
        return False
    cur_low, cur_high = low, high
    for i in range(1, n):
        low_i = max(0, H - D[i])
        high_i = min(U[i], H)
        if low_i > high_i:
            return False
        new_low = max(low_i, cur_low - X)
        new_high = min(high_i, cur_high + X)
        if new_low > new_high:
            return False
        cur_low, cur_high = new_low, new_high
    return True

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    U = []
    D = []
    total = 0
    maxH = 10**20  # sufficiently large
    for _ in range(N):
        u = int(next(it))
        d = int(next(it))
        U.append(u)
        D.append(d)
        total += u + d
        maxH = min(maxH, u + d)
    lo = 0
    hi = maxH
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid, U, D, X):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    # Minimum cost is total - N * best
    print(total - N * best)

if __name__ == "__main__":
    solve()
