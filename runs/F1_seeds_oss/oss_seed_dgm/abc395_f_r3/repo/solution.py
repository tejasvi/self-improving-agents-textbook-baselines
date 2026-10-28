# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    U = [0] * N
    D = [0] * N
    total_sum = 0
    min_sum = None
    for i in range(N):
        u = int(next(it))
        d = int(next(it))
        U[i] = u
        D[i] = d
        s = u + d
        total_sum += s
        if min_sum is None or s < min_sum:
            min_sum = s

    def feasible(H: int) -> bool:
        # Determine if we can choose U' satisfying constraints for given H
        low = max(0, H - D[0])
        high = min(U[0], H)
        if low > high:
            return False
        for i in range(1, N):
            L = max(0, H - D[i])
            R = min(U[i], H)
            if L > R:
                return False
            new_low = max(L, low - X)
            new_high = min(R, high + X)
            if new_low > new_high:
                return False
            low, high = new_low, new_high
        return True

    # Binary search for maximum feasible H
    lo = 0
    hi = min_sum
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    H_opt = lo
    answer = total_sum - N * H_opt
    print(answer)

if __name__ == "__main__":
    solve()
