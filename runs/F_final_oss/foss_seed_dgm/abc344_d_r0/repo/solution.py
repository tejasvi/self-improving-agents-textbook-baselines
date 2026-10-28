# Write your solution here. Read from stdin, write to stdout.
import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    # First token is T (string)
    it = iter(data)
    T = next(it)
    n = int(next(it))
    bags = []
    for _ in range(n):
        a = int(next(it))
        strings = [next(it) for __ in range(a)]
        bags.append(strings)
    L = len(T)
    INF = 10**9
    dp = [INF] * (L + 1)
    dp[0] = 0
    for strings in bags:
        newdp = dp[:]  # skipping this bag
        for s in strings:
            slen = len(s)
            for pos in range(L + 1):
                if dp[pos] == INF:
                    continue
                if pos + slen <= L and T.startswith(s, pos):
                    # can place s here
                    if dp[pos] + 1 < newdp[pos + slen]:
                        newdp[pos + slen] = dp[pos] + 1
        dp = newdp
    ans = dp[L]
    if ans == INF:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
