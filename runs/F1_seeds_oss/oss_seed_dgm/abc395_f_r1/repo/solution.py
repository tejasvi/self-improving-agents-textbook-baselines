# Write your solution here. Read from stdin, write to stdout.
import sys

def feasible(H, a, b, X):
    N = len(a)
    low = max(0, H - b[0])
    high = min(a[0], H)
    if low > high:
        return False
    for i in range(1, N):
        Li = max(0, H - b[i])
        Ri = min(a[i], H)
        low = max(Li, low - X)
        high = min(Ri, high + X)
        if low > high:
            return False
    return True

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    a = []
    b = []
    total = 0
    min_sum = 10**20
    for _ in range(N):
        u = int(next(it))
        d = int(next(it))
        a.append(u)
        b.append(d)
        total += u + d
        if u + d < min_sum:
            min_sum = u + d
    lo = 0
    hi = min_sum
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid, a, b, X):
            lo = mid
        else:
            hi = mid - 1
    answer = total - N * lo
    print(answer)

if __name__ == "__main__":
    solve()
