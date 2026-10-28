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
        strings = data[idx:idx + a]
        idx += a
        new_dp = dp[:]  # do nothing
        for j in range(L + 1):
            if dp[j] == INF:
                continue
            for s in strings:
                k = len(s)
                if j + k <= L and T.startswith(s, j):
                    if dp[j] + 1 < new_dp[j + k]:
                        new_dp[j + k] = dp[j] + 1
        dp = new_dp
    print(dp[L] if dp[L] != INF else -1)


main()
