import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    T = data[pos]
    pos += 1
    n = int(data[pos])
    pos += 1
    L = len(T)
    INF = float('inf')
    dp = [INF] * (L + 1)
    dp[0] = 0
    for _ in range(n):
        a = int(data[pos])
        pos += 1
        strs = set(data[pos:pos + a])
        pos += a
        new = dp[:]
        for j in range(1, L + 1):
            best = new[j]
            for s in strs:
                k = len(s)
                if k <= j and dp[j - k] + 1 < best and T[j - k:j] == s:
                    best = dp[j - k] + 1
            new[j] = best
        dp = new
    ans = dp[L]
    print(-1 if ans == INF else ans)


main()
