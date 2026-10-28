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
        strs = set(data[idx: idx + a])
        idx += a
        new = dp[:]
        for j in range(1, L + 1):
            best = new[j]
            for s in strs:
                k = len(s)
                if k <= j and dp[j - k] + 1 < best and T[j - k: j] == s:
                    best = dp[j - k] + 1
            new[j] = best
        dp = new
    ans = dp[L]
    print(ans if ans != INF else -1)


main()
