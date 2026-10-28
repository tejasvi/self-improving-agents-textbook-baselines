import sys


def main():
    data = sys.stdin.read().split()
    T = data[0]
    n = int(data[1])
    idx = 2
    L = len(T)
    INF = float('inf')
    dp = [INF] * (L + 1)
    dp[0] = 0
    for _ in range(n):
        a = int(data[idx])
        idx += 1
        strs = data[idx:idx + a]
        idx += a
        new = dp[:]  # do nothing
        for j in range(L + 1):
            if dp[j] == INF:
                continue
            for s in strs:
                k = j + len(s)
                if k <= L and T[j:k] == s and dp[j] + 1 < new[k]:
                    new[k] = dp[j] + 1
        dp = new
    ans = dp[L]
    print(-1 if ans == INF else ans)


main()
