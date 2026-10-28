# Write your solution here. Read from stdin, write to stdout.
import sys

def min_cost_for_capacity(C, A, P, B, Q):
    # Only S machines
    cost = ((C + A - 1) // A) * P
    # Only T machines
    cost = min(cost, ((C + B - 1) // B) * Q)
    # Mix: iterate limited counts of T
    for t in range(A):  # t is number of T machines (0..A-1)
        remain = C - B * t
        if remain <= 0:
            s_needed = 0
        else:
            s_needed = (remain + A - 1) // A
        cur = t * Q + s_needed * P
        if cur < cost:
            cost = cur
    # Mix: iterate limited counts of S
    for s in range(B):  # s is number of S machines (0..B-1)
        remain = C - A * s
        if remain <= 0:
            t_needed = 0
        else:
            t_needed = (remain + B - 1) // B
        cur = s * P + t_needed * Q
        if cur < cost:
            cost = cur
    return cost

def feasible(C, processes, X):
    total = 0
    for A, P, B, Q in processes:
        cost = min_cost_for_capacity(C, A, P, B, Q)
        total += cost
        if total > X:
            return False
    return total <= X

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    processes = []
    for _ in range(N):
        A = int(next(it)); P = int(next(it)); B = int(next(it)); Q = int(next(it))
        processes.append((A, P, B, Q))
    # Binary search for maximum feasible C
    lo = 0
    hi = 10**12 + 1  # exclusive upper bound
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if feasible(mid, processes, X):
            lo = mid
        else:
            hi = mid
    print(lo)

if __name__ == "__main__":
    solve()
