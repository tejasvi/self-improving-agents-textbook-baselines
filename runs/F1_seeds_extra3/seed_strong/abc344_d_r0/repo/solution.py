import sys


def main():
    data = sys.stdin.read().split()
    T = data[0]
    n = int(data[1])
    pos = 2
    m = len(T)
    INF = float("inf")
    dp = [INF] * (m + 1)
    dp[0] = 0
    for _ in range(n):
        a = int(data[pos])
        pos += 1
        strs = data[pos:pos + a]
        pos += a
        new = dp[:]
        for s in set(strs):
            L = len(s)
            for j in range(L, m + 1):
                if dp[j - L] + 1 < new[j] and T[j - L:j] == s:
                    new[j] = dp[j - L] + 1
        dp = new
    ans = dp[m]
    print(-1 if ans == INF else ans)


main()
