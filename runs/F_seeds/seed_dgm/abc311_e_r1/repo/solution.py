import sys


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])

    holed_rows = [bytearray(W) for _ in range(H)]
    for k in range(N):
        a = int(data[3 + 2 * k]) - 1
        b = int(data[4 + 2 * k]) - 1
        holed_rows[a][b] = 1

    # Process rows bottom-up.
    # below[j]: consecutive non-holed cells going down from (i, j)
    # g[j]: largest holeless square with top-left corner at (i, j)
    #   g = 0 if holed, else min(g[i+1][j+1] + 1, right[j], below[j])
    below = [0] * W
    prev_g = [0] * (W + 1)  # sentinel for column W
    total = 0
    for i in range(H - 1, -1, -1):
        hr = holed_rows[i]
        below = [0 if hr[j] else below[j] + 1 for j in range(W)]
        right = [0] * W
        run = 0
        for j in range(W - 1, -1, -1):
            run = 0 if hr[j] else run + 1
            right[j] = run
        cur = [0] * W
        for j in range(W):
            if hr[j]:
                continue
            v = prev_g[j + 1] + 1
            if right[j] < v:
                v = right[j]
            if below[j] < v:
                v = below[j]
            cur[j] = v
        total += sum(cur)
        prev_g = cur + [0]
    print(total)


main()
