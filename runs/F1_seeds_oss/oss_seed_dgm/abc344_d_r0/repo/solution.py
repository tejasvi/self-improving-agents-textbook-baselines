# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    # First token is T string
    it = iter(data)
    T = next(it)
    L = len(T)
    N = int(next(it))
    bags = []
    for _ in range(N):
        Ai = int(next(it))
        strs = [next(it) for __ in range(Ai)]
        bags.append(strs)
    INF = 10**9
    dp = [INF] * (L + 1)
    dp[0] = 0
    for bag in bags:
        # copy for skipping case
        ndp = dp[:]  # skipping bag keeps same cost
        for pos in range(L + 1):
            if dp[pos] == INF:
                continue
            # try each string in current bag
            for s in bag:
                l = len(s)
                if pos + l > L:
                    continue
                if T[pos:pos + l] == s:
                    if ndp[pos + l] > dp[pos] + 1:
                        ndp[pos + l] = dp[pos] + 1
        dp = ndp
    ans = dp[L]
    if ans == INF:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
