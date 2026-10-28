import sys


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    # holed[i] is a set of 0-indexed columns in row i that are holed
    holed = [bytearray(W + 1) for _ in range(H)]
    p = 3
    for _ in range(N):
        a = int(data[p]) - 1
        b = int(data[p + 1]) - 1
        holed[a][b] = 1
        p += 2
    # dp[j] = largest holeless square with top-left at (i, j) (0 if holed).
    # dp[j] = 1 + min(below[j], below[j+1], cur[j+1]) for non-holed cells.
    below = [0] * (W + 1)
    total = 0
    for i in range(H - 1, -1, -1):
        h = holed[i]
        g = [min(below[j], below[j + 1]) for j in range(W)]
        cur = [0] * (W + 1)
        right = 0  # cur[j+1]
        s = 0
        for j in range(W - 1, -1, -1):
            if h[j]:
                v = 0
            else:
                v = g[j] if g[j] < right else right
                v += 1
            cur[j] = v
            right = v
            s += v
        total += s
        below = cur
    print(total)


main()
