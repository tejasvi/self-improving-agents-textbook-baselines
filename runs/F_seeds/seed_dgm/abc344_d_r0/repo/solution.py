import sys


def main():
    data = sys.stdin.read().split()
    pos = 0
    T = data[pos]; pos += 1
    n = int(data[pos]); pos += 1
    L = len(T)
    INF = float('inf')
    dp = [INF] * (L + 1)
    dp[0] = 0
    for _ in range(n):
        a = int(data[pos]); pos += 1
        strs = data[pos:pos + a]
        pos += a
        ndp = dp[:]  # do nothing
        for j in range(L + 1):
            if dp[j] == INF:
                continue
            for s in strs:
                k = j + len(s)
                if k <= L and T[j:k] == s and dp[j] + 1 < ndp[k]:
                    ndp[k] = dp[j] + 1
        dp = ndp
    ans = dp[L]
    print(-1 if ans == INF else ans)


main()
