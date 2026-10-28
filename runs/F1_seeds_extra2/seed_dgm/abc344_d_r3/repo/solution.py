import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    T = data[idx]; idx += 1
    n = int(data[idx]); idx += 1
    L = len(T)
    INF = float("inf")
    dp = [INF] * (L + 1)
    dp[0] = 0
    for _ in range(n):
        a = int(data[idx]); idx += 1
        strs = set(data[idx: idx + a]); idx += a
        new = dp[:]
        for j in range(L + 1):
            if dp[j] == INF:
                continue
            for s in strs:
                e = j + len(s)
                if e <= L and T.startswith(s, j):
                    if dp[j] + 1 < new[e]:
                        new[e] = dp[j] + 1
        dp = new
    print(dp[L] if dp[L] != INF else -1)


main()
