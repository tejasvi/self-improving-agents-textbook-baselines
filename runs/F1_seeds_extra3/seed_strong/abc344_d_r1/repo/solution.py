import sys


def main():
    data = sys.stdin.read().split()
    T = data[0]
    n = int(data[1])
    idx = 2
    L = len(T)
    INF = float("inf")
    dp = [INF] * (L + 1)
    dp[0] = 0
    for _ in range(n):
        a = int(data[idx])
        idx += 1
        strs = data[idx:idx + a]
        idx += a
        ndp = dp[:]
        for s in set(strs):
            m = len(s)
            for j in range(m, L + 1):
                if dp[j - m] + 1 < ndp[j] and T[j - m:j] == s:
                    ndp[j] = dp[j - m] + 1
        dp = ndp
    ans = dp[L]
    print(ans if ans != INF else -1)


main()
