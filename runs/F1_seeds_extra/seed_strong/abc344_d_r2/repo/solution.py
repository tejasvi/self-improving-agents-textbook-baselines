import sys


def main():
    data = sys.stdin.read().split()
    T = data[0]
    n = int(data[1])
    pos = 2
    L = len(T)
    INF = float("inf")
    dp = [INF] * (L + 1)
    dp[0] = 0
    for _ in range(n):
        a = int(data[pos])
        pos += 1
        strs = data[pos:pos + a]
        pos += a
        ndp = dp[:]  # do nothing
        for j in range(L + 1):
            cur = dp[j]
            if cur == INF:
                continue
            c = cur + 1
            for s in strs:
                e = j + len(s)
                if e <= L and ndp[e] > c and T.startswith(s, j):
                    ndp[e] = c
        dp = ndp
    ans = dp[L]
    print(-1 if ans == INF else ans)


main()
