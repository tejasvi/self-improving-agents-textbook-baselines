import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    q = int(data[1])
    ks = [int(x) for x in data[2:2 + q]]

    # dp[r][c]: bitset of achievable "free cell" counts using at most r rows
    # and at most c columns, where free cells come from disjoint blocks
    # p x q' (p, q' >= 2), block uses p rows and q' columns.
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    for r in range(n + 1):
        for c in range(n + 1):
            dp[r][c] = 1  # area 0 always achievable
    for r in range(2, n + 1):
        for c in range(2, n + 1):
            acc = dp[r - 1][c] | dp[r][c - 1]
            for p in range(2, r + 1):
                for qq in range(2, c + 1):
                    acc |= dp[r - p][c - qq] << (p * qq)
            dp[r][c] = acc
    # ensure monotonicity for r<2 or c<2 cases (only area 0 there)
    best = dp[n][n]

    out = []
    total = n * n
    for k in ks:
        m = total - k
        if 0 <= m <= total and (best >> m) & 1:
            out.append("Yes")
        else:
            out.append("No")
    sys.stdout.write("\n".join(out) + "\n")


main()
