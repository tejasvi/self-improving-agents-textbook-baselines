import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    T = data[pos]; pos += 1
    n = int(data[pos]); pos += 1
    m = len(T)
    INF = float("inf")
    dp = [INF] * (m + 1)
    dp[0] = 0
    for _ in range(n):
        a = int(data[pos]); pos += 1
        strs = data[pos:pos + a]
        pos += a
        new = dp[:]  # do nothing
        for j in range(1, m + 1):
            best = new[j]
            for s in strs:
                L = len(s)
                if L <= j and dp[j - L] + 1 < best and T[j - L:j] == s:
                    best = dp[j - L] + 1
            new[j] = best
        dp = new
    ans = dp[m]
    print(-1 if ans == INF else ans)


main()
