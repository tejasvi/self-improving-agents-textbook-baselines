import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    q = int(data[1])
    ks = [int(x) for x in data[2:2 + q]]

    # dp[r][c] = bitmask of achievable sums S = sum(a*b) using at most r rows
    # and at most c columns, where each block has a>=2 rows and b>=2 cols.
    # Achievable "non-fixed" counts are such sums; fixed = n*n - S.
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for r in range(n + 1):
        for c in range(n + 1):
            if r == 0 and c == 0:
                dp[r][c] = 1
                continue
            v = 0
            if r > 0:
                v |= dp[r - 1][c]
            if c > 0:
                v |= dp[r][c - 1]
            for a in range(2, r + 1):
                row = dp[r - a]
                for b in range(2, c + 1):
                    v |= row[c - b] << (a * b)
            dp[r][c] = v
    ok = dp[n][n]
    total = n * n

    out = []
    for k in ks:
        s = total - k
        if 0 <= s <= total and (ok >> s) & 1:
            out.append("Yes")
        else:
            out.append("No")
    sys.stdout.write("\n".join(out) + "\n")


main()
