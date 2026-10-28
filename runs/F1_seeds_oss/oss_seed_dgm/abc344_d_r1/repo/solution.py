# Write your solution here. Read from stdin, write to stdout.

import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    T = next(it)
    N = int(next(it))
    bags = []
    for _ in range(N):
        A = int(next(it))
        strings = [next(it) for _ in range(A)]
        bags.append(strings)
    L = len(T)
    INF = 10**9
    # dp[pos] = minimum cost after processing previous bag
    dp_prev = [INF] * (L + 1)
    dp_prev[0] = 0
    for idx, bag in enumerate(bags, 1):
        dp_curr = [INF] * (L + 1)
        # Option: do nothing, carry over
        for pos in range(L + 1):
            if dp_prev[pos] < dp_curr[pos]:
                dp_curr[pos] = dp_prev[pos]
        # Option: pick one string from this bag
        for pos in range(L + 1):
            if dp_prev[pos] == INF:
                continue
            for s in bag:
                l = len(s)
                if pos + l <= L and T.startswith(s, pos):
                    new_cost = dp_prev[pos] + 1
                    if new_cost < dp_curr[pos + l]:
                        dp_curr[pos + l] = new_cost
        dp_prev = dp_curr
    ans = dp_prev[L]
    print(ans if ans != INF else -1)

if __name__ == "__main__":
    solve()
