class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)
        INF = float("inf")

        # cost[i][j]: min changes to make s[i..j] (inclusive) a semi-palindrome
        cost = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                L = j - i + 1
                best = INF
                for d in range(1, L):
                    if L % d:
                        continue
                    changes = 0
                    for r in range(d):
                        # residue class starting at i + r with step d
                        a, b = i + r, i + r + d * ((L - 1 - r) // d)
                        while a < b:
                            if s[a] != s[b]:
                                changes += 1
                            a += d
                            b -= d
                    if changes < best:
                        best = changes
                cost[i][j] = best

        # dp[t][j]: min cost to split s[0..j-1] into t parts
        dp = [[INF] * (n + 1) for _ in range(k + 1)]
        dp[0][0] = 0
        for t in range(1, k + 1):
            for j in range(1, n + 1):
                best = INF
                for i in range(t - 1, j):
                    if dp[t - 1][i] == INF:
                        continue
                    # segment s[i..j-1]
                    if i == j - 1:
                        continue  # length-1 has no valid d
                    c = dp[t - 1][i] + cost[i][j - 1]
                    if c < best:
                        best = c
                dp[t][j] = best
        return int(dp[k][n])
