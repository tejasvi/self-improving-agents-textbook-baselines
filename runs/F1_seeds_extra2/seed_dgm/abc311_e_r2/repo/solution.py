import sys


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    # free[i][j] = 1 if square (i, j) (0-indexed) is not holed
    free = [[1] * W for _ in range(H)]
    p = 3
    for _ in range(N):
        a = int(data[p]) - 1
        b = int(data[p + 1]) - 1
        free[a][b] = 0
        p += 2

    # dp[i][j] = largest holeless square with top-left corner (i, j)
    # dp[i][j] = min(dp[i+1][j+1] + 1, R[i][j], D[i][j])
    # R = run of free cells to the right (incl.), D = run of free cells downward (incl.)
    D_below = [0] * W
    dp_next = [0] * (W + 1)  # sentinel at index W
    total = 0
    for i in range(H - 1, -1, -1):
        row = free[i]
        D = [d + 1 if f else 0 for d, f in zip(D_below, row)]
        R = [0] * W
        r = 0
        for j in range(W - 1, -1, -1):
            r = r + 1 if row[j] else 0
            R[j] = r
        diag = [x + 1 for x in dp_next[1:]]
        cur = [min(a, b, c) for a, b, c in zip(diag, R, D)]
        total += sum(cur)
        D_below = D
        dp_next = cur + [0]
    print(total)


if __name__ == "__main__":
    main()
