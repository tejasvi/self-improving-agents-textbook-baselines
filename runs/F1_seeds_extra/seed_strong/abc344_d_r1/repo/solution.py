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
        strs = data[idx: idx + a]
        idx += a
        new = dp[:]  # do nothing
        for j in range(1, L + 1):
            best = new[j]
            for s in strs:
                ls = len(s)
                if ls <= j and dp[j - ls] + 1 < best and T[j - ls: j] == s:
                    best = dp[j - ls] + 1
            new[j] = best
        dp = new
    ans = dp[L]
    print(ans if ans != INF else -1)


main()
