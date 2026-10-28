import sys
from itertools import accumulate


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holed = [bytearray(b'\x01') * W for _ in range(H)]  # 1 = free
    idx = 3
    for _ in range(N):
        a = int(data[idx]) - 1
        b = int(data[idx + 1]) - 1
        idx += 2
        holed[a][b] = 0

    up = [0] * W
    prev = [0] * W  # dp of previous row (bottom-right formulation)
    total = 0
    step = lambda a, f: (a + 1) if f else 0
    for i in range(H):
        row = holed[i]
        up = [u + 1 if f else 0 for u, f in zip(up, row)]
        left = list(accumulate(row, step, initial=0))
        del left[0]
        # diag[j] = prev[j-1] + 1 for j>=1, diag[0] = 1 if free ... (no j-1 => size 1 bounded by left/up)
        diag = [1]
        diag.extend(p + 1 for p in prev[:-1])
        cur = list(map(min, up, left, diag))
        total += sum(cur)
        prev = cur
    print(total)


main()
