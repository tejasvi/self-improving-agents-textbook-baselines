import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); Q = int(data[1])
    Ks = [int(x) for x in data[2:2 + Q]]
    # dp[r][c]: bitset over m (number of non-fixed cells) achievable using
    # exactly r rows and c columns in disjoint a x b blocks (a,b >= 2).
    dp = [[0] * (N + 1) for _ in range(N + 1)]
    dp[0][0] = 1
    for r in range(N + 1):
        for c in range(N + 1):
            cur = dp[r][c]
            if not cur:
                continue
            for a in range(2, N - r + 1):
                row = dp[r + a]
                for b in range(2, N - c + 1):
                    row[c + b] |= cur << (a * b)
    total = 0
    for r in range(N + 1):
        for c in range(N + 1):
            total |= dp[r][c]
    achievable = set()
    m = 0
    t = total
    while t:
        if t & 1:
            achievable.add(N * N - m)
        t >>= 1
        m += 1
    out = ["Yes" if k in achievable else "No" for k in Ks]
    sys.stdout.write("\n".join(out) + "\n")

main()
