import sys


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    # holes[i] is a bytearray row: 1 if (i, j) is holed (1-indexed columns)
    holes = [bytearray(W + 1) for _ in range(H + 1)]
    idx = 3
    for _ in range(N):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        holes[a][b] = 1
    # dp[j] = side of largest holeless square with bottom-right corner (i, j)
    prev = [0] * (W + 1)
    total = 0
    for i in range(1, H + 1):
        row = holes[i]
        cur = [0] * (W + 1)
        left = 0
        diag = 0  # prev[j-1]
        for j in range(1, W + 1):
            up = prev[j]
            if row[j]:
                v = 0
            else:
                v = up
                if left < v:
                    v = left
                if diag < v:
                    v = diag
                v += 1
            cur[j] = v
            total += v
            left = v
            diag = up
        prev = cur
    print(total)


main()
