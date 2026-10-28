import sys
from itertools import accumulate

def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holes = [bytearray(b"\x01") * (W + 1) for _ in range(H + 1)]  # 1 = free
    for r in holes: r[0] = 0
    for k in range(N):
        a = int(data[3 + 2 * k]); b = int(data[4 + 2 * k])
        holes[a][b] = 0
    U = [0] * (W + 1)           # consecutive free cells upward, index 0 is padding
    prev = [0] * (W + 1)        # dp of previous row
    total = 0
    for i in range(1, H + 1):
        free = holes[i]
        U = [u + 1 if f else 0 for u, f in zip(U, free)]
        # L[j]: consecutive free cells leftward ending at j (j>=1)
        L = list(accumulate(free, lambda acc, f: acc + 1 if f else 0))
        # diag[j] = prev[j-1] + 1
        cur = [0] + [min(u, l, p + 1) for u, l, p in zip(U[1:], L[1:], prev[:-1])]
        # cur[j] for j>=1; cur[0] padding must be 0
        cur[0] = 0
        total += sum(cur)
        prev = cur
    print(total)

main()
