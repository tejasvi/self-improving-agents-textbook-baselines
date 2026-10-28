import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    # First token is T (may contain newline but split handles)
    it = iter(data)
    T = next(it)
    N = int(next(it))
    bags = []
    for _ in range(N):
        Ai = int(next(it))
        strs = [next(it) for __ in range(Ai)]
        bags.append(strs)
    L = len(T)
    INF = 10**9
    # dp[pos] = min cost after processing previous bags
    dp = [INF] * (L + 1)
    dp[0] = 0
    for bag in bags:
        new_dp = [INF] * (L + 1)
        for pos in range(L + 1):
            if dp[pos] == INF:
                continue
            # skip this bag
            if dp[pos] < new_dp[pos]:
                new_dp[pos] = dp[pos]
            # try each string in bag
            for w in bag:
                nl = len(w)
                np = pos + nl
                if np <= L and T[pos:np] == w:
                    cost = dp[pos] + 1
                    if cost < new_dp[np]:
                        new_dp[np] = cost
        dp = new_dp
    ans = dp[L]
    if ans == INF:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
