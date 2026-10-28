import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    X = [int(data[1 + 2 * i]) for i in range(n)]
    Y = [int(data[2 + 2 * i]) for i in range(n)]
    # Yx[x] = Y-value of the point whose X equals x; sentinels at x=0 and x=n+1
    Yx = [0] * (n + 2)
    for i in range(n):
        Yx[X[i]] = Y[i]
    Yx[0] = n + 1  # virtual start S = (0, n+1)
    Yx[n + 1] = 0  # virtual end   T = (n+1, 0)
    # C[x][y] = number of points with X<=x and Y<=y (points only at 1..n)
    C = [[0] * (n + 2) for _ in range(n + 2)]
    for x in range(1, n + 1):
        y0 = Yx[x]
        row, prev = C[x], C[x - 1]
        run = 0
        for y in range(n + 2):
            if y == y0:
                run += 1
            row[y] = prev[y] + run

    def good(ax, bx, by, ay):
        # rectangle x in (ax,bx), y in (by,ay); every point needs a mono partner inside
        for px in range(ax + 1, bx):
            py = Yx[px]
            if not (by < py < ay):
                continue
            # SW partner: x in (ax,px), y in (by,py)
            sw = C[px - 1][py - 1] - C[ax][py - 1] - C[px - 1][by] + C[ax][by]
            if sw > 0:
                continue
            # NE partner: x in (px,bx), y in (py,ay)
            ne = C[bx - 1][ay - 1] - C[px][ay - 1] - C[bx - 1][py] + C[px][py]
            if ne > 0:
                continue
            return False
        return True

    # nodes indexed by X coordinate 0..n+1; a node exists at each x
    dp = [0] * (n + 2)
    dp[0] = 1
    for b in range(1, n + 2):
        by = Yx[b]
        acc = 0
        for a in range(0, b):
            if dp[a] and Yx[a] > by and good(a, b, by, Yx[a]):
                acc += dp[a]
        dp[b] = acc % MOD
    print(dp[n + 1] % MOD)

main()
