import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    N = int(data[2])
    holes = [[False] * (W + 2) for _ in range(H + 2)]
    idx = 3
    for _ in range(N):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        holes[a][b] = True

    # s[j]: size of the largest holeless square whose bottom-right corner is (i, j)
    # for the current row i; prev holds the row above (i-1).
    prev = [0] * (W + 2)
    total = 0
    for i in range(1, H + 1):
        cur = [0] * (W + 2)
        row = holes[i]
        for j in range(1, W + 1):
            if not row[j]:
                a = prev[j]
                b = prev[j - 1]
                c = cur[j - 1]
                if b < a:
                    a = b
                if c < a:
                    a = c
                cur[j] = a + 1
                total += a + 1
        prev = cur
    print(total)


main()
