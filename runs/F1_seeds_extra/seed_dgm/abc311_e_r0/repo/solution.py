import sys
from itertools import accumulate


def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holes = [bytearray(b'\x01') * (W + 1) for _ in range(H + 1)]  # 1 = free
    for k in range(N):
        a = int(data[3 + 2 * k])
        b = int(data[4 + 2 * k])
        holes[a][b] = 0
    up = [0] * (W + 1)        # consecutive free cells above (column-wise)
    prev = [0] * (W + 1)      # dp of previous row, index j (1-based), prev[0]=0
    total = 0
    for i in range(1, H + 1):
        row = holes[i]
        # up run lengths
        up = [u + 1 if f else 0 for u, f in zip(up, row)]
        # left run lengths
        left = [0] + list(accumulate(row[1:], lambda a, f: a + 1 if f else 0))
        # dp[j] = min(up[j], left[j], prev[j-1] + 1)
        shifted = [0] + [x + 1 for x in prev[:-1]]
        cur = list(map(min, up, left, shifted))
        cur[0] = 0
        total += sum(cur)
        prev = cur
    print(total)


main()
