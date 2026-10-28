import sys


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holed = [bytearray(W + 1) for _ in range(H + 1)]  # holed[i][j], 1-indexed
    idx = 3
    for _ in range(N):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        holed[a][b] = 1

    up = [0] * (W + 1)      # consecutive non-holed cells above (inclusive) in column j
    prev = [0] * (W + 1)    # dp of previous row
    total = 0
    for i in range(1, H + 1):
        hr = holed[i]
        # up run lengths
        up = [0 if hr[j] else up[j] + 1 for j in range(W + 1)]
        cur = [0] * (W + 1)
        left = 0  # consecutive non-holed cells to the left (inclusive)
        for j in range(1, W + 1):
            if hr[j]:
                left = 0
                continue
            left += 1
            d = prev[j - 1] + 1
            u = up[j]
            if u < d:
                d = u
            if left < d:
                d = left
            cur[j] = d
            total += d
        prev = cur
    print(total)


main()
