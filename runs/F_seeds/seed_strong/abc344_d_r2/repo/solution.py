import sys


def main():
    data = sys.stdin.read().split()
    T = data[0]
    n = int(data[1])
    pos = 2
    L = len(T)
    INF = float('inf')
    dp = [INF] * (L + 1)
    dp[0] = 0
    for _ in range(n):
        a = int(data[pos])
        pos += 1
        strs = data[pos:pos + a]
        pos += a
        new = dp[:]
        for j in range(L + 1):
            cur = dp[j]
            if cur == INF:
                continue
            for s in strs:
                k = j + len(s)
                if k <= L and cur + 1 < new[k] and T[j:k] == s:
                    new[k] = cur + 1
        dp = new
    ans = dp[L]
    print(ans if ans != INF else -1)


main()
