# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    import sys
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

    # function to compute minimal cost to achieve at least capacity C for a single process
    def min_cost_for_process(A, P, B, Q, C):
        # iterate over possible number of type T machines (t) from 0 to A-1 (inclusive)
        # compute needed S machines
        best = 10**30
        # also iterate over s up to B-1 to be safe (optional)
        for t in range(A):  # A <= 100
            # capacity contributed by t machines of type T
            cap_t = B * t
            if cap_t >= C:
                s_needed = 0
            else:
                # remaining capacity needed
                rem = C - cap_t
                s_needed = (rem + A - 1) // A  # ceil division
            cost = s_needed * P + t * Q
            if cost < best:
                best = cost
        # also iterate over s up to B-1 (symmetry) to ensure optimality when the cheap type is T
        for s in range(B):
            cap_s = A * s
            if cap_s >= C:
                t_needed = 0
            else:
                rem = C - cap_s
                t_needed = (rem + B - 1) // B
            cost = s * P + t_needed * Q
            if cost < best:
                best = cost
        return best

    # check if capacity C is achievable within budget X
    def feasible(C):
        total = 0
        for (A, P, B, Q) in processes:
            cost = min_cost_for_process(A, P, B, Q, C)
            total += cost
            if total > X:
                return False
        return total <= X

    # binary search maximum C
    lo = 0
    hi = 10**12  # sufficiently large upper bound
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

if __name__ == "__main__":
    solve()
