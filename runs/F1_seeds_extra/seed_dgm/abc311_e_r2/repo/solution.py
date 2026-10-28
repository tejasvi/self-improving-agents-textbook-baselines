import sys


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holed = [bytearray(W) for _ in range(H)]
    idx = 3
    for _ in range(N):
        a = int(data[idx]) - 1
        b = int(data[idx + 1]) - 1
        idx += 2
        holed[a][b] = 1

    # dp[i][j] = largest holeless square with bottom-right corner at (i, j)
    # dp[i][j] = min(up, left, dp[i-1][j-1] + 1); holed cells give 0.
    up = [0] * W
    prev = [0] * (W + 1)  # prev[j+1] = dp of previous row at column j
    total = 0
    for i in range(H):
        row = holed[i]
        cur = [0] * (W + 1)
        left = 0
        for j in range(W):
            if row[j]:
                up[j] = 0
                left = 0
                continue
            u = up[j] + 1
            up[j] = u
            left += 1
            m = u if u < left else left
            d = prev[j] + 1
            if d < m:
                m = d
            cur[j + 1] = m
            total += m
        prev = cur
    print(total)


main()
