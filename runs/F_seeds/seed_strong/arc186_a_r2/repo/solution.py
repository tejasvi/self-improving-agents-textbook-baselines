import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    q = int(data[1])
    ks = [int(x) for x in data[2:2 + q]]

    # Free cells F = N^2 - K. Achievable F are sums of products a*b over
    # blocks with a, b >= 2 whose row-total sum(a) <= N and column-total sum(b) <= N.
    # dp[x][y] = bitset (python int) of achievable F with exact sums x (rows), y (cols).
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for x in range(n + 1):
        for y in range(n + 1):
            if x == 0 and y == 0:
                continue
            acc = 0
            for a in range(2, x + 1):
                row = dp[x - a]
                for b in range(2, y + 1):
                    v = row[y - b]
                    if v:
                        acc |= v << (a * b)
            dp[x][y] = acc
    achievable = 0
    for x in range(n + 1):
        for y in range(n + 1):
            achievable |= dp[x][y]

    out = []
    total = n * n
    for k in ks:
        f = total - k
        if 0 <= f <= total and (achievable >> f) & 1:
            out.append("Yes")
        else:
            out.append("No")
    sys.stdout.write("\n".join(out) + "\n")


main()
