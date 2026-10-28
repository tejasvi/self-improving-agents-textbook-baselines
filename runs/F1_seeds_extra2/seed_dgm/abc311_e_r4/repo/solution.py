import sys


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holed = bytearray((H + 1) * (W + 1))  # index i*(W+1)+j, 1-based
    idx = 3
    stride = W + 1
    for _ in range(N):
        a = int(data[idx])
        b = int(data[idx + 1])
        idx += 2
        holed[a * stride + b] = 1

    prev = [0] * (W + 1)
    total = 0
    for i in range(1, H + 1):
        cur = [0] * (W + 1)
        base = i * stride
        left = 0  # cur[j-1]
        diag = 0  # prev[j-1]
        for j in range(1, W + 1):
            up = prev[j]
            if holed[base + j]:
                v = 0
            else:
                v = up
                if diag < v:
                    v = diag
                if left < v:
                    v = left
                v += 1
            cur[j] = v
            total += v
            left = v
            diag = up
        prev = cur
    print(total)


main()
