import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    N = int(data[2])
    holes = [bytearray(W + 1) for _ in range(H + 1)]
    idx = 3
    for _ in range(N):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        holes[a][b] = 1

    prev = [0] * (W + 1)
    total = 0
    for i in range(1, H + 1):
        hrow = holes[i]
        cur = [0] * (W + 1)
        left = 0
        for j in range(1, W + 1):
            if hrow[j]:
                left = 0
            else:
                up = prev[j]
                dg = prev[j - 1]
                m = up if up < left else left
                if dg < m:
                    m = dg
                left = m + 1
            cur[j] = left
        total += sum(cur)
        prev = cur
    print(total)


main()
