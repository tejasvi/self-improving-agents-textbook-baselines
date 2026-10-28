import sys


def main():
    data = sys.stdin.read().split()
    T = data[0]
    n = int(data[1])
    L = len(T)
    INF = float("inf")
    dp = [INF] * (L + 1)
    dp[0] = 0
    pos = 2
    for _ in range(n):
        a = int(data[pos])
        strs = data[pos + 1: pos + 1 + a]
        pos += 1 + a
        new = dp[:]
        for s in set(strs):
            m = len(s)
            for j in range(m, L + 1):
                if dp[j - m] + 1 < new[j] and T[j - m:j] == s:
                    new[j] = dp[j - m] + 1
        dp = new
    ans = dp[L]
    print(ans if ans != INF else -1)


main()
