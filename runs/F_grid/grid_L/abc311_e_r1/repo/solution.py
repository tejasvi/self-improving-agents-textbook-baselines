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

    up = [0] * (W + 1)      # consecutive free cells above (including current row)
    prev = [0] * (W + 1)    # dp values of previous row
    total = 0
    for i in range(1, H + 1):
        row = holes[i]
        cur = [0] * (W + 1)
        left = 0
        for j in range(1, W + 1):
            if row[j]:
                up[j] = 0
                left = 0
            else:
                up[j] += 1
                left += 1
                v = prev[j - 1] + 1
                if up[j] < v:
                    v = up[j]
                if left < v:
                    v = left
                cur[j] = v
                total += v
        prev = cur
    sys.stdout.write(str(total) + "\n")


main()
