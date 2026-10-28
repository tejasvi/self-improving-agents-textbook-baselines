class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)
        INF = float("inf")

        # cost[i][j]: min changes to make s[i..j] (inclusive) a semi-palindrome
        cost = [[INF] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                length = j - i + 1
                best = INF
                for d in range(1, length):
                    if length % d != 0:
                        continue
                    changes = 0
                    for r in range(d):
                        # indices i+r, i+r+d, ... within the substring
                        lo, hi = i + r, i + length - d + r
                        while lo < hi:
                            if s[lo] != s[hi]:
                                changes += 1
                            lo += d
                            hi -= d
                    if changes < best:
                        best = changes
                cost[i][j] = best

        # dp[p][e]: min cost to split s[0..e-1] into p semi-palindromes
        dp = [[INF] * (n + 1) for _ in range(k + 1)]
        dp[0][0] = 0
        for p in range(1, k + 1):
            for e in range(p, n + 1):
                best = INF
                for st in range(p - 1, e):
                    if dp[p - 1][st] == INF:
                        continue
                    c = cost[st][e - 1]
                    if c == INF:
                        continue
                    v = dp[p - 1][st] + c
                    if v < best:
                        best = v
                dp[p][e] = best
        return int(dp[k][n])
