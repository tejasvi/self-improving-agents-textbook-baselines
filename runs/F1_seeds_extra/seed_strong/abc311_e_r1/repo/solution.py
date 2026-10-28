import sys

try:
    (0).bit_count()
    def popcount(x):
        return x.bit_count()
except AttributeError:
    def popcount(x):
        return bin(x).count('1')


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); N = int(data[2])
    holes = [0] * H  # bitmask of holed columns per row (0-indexed)
    idx = 3
    for _ in range(N):
        a = int(data[idx]) - 1
        b = int(data[idx + 1]) - 1
        idx += 2
        holes[a] |= 1 << b
    full = (1 << W) - 1
    # F[i] bit j set iff the k x k square with top-left (i, j) is holeless (k=1 initially)
    F = [full ^ holes[i] for i in range(H)]
    total = sum(popcount(x) for x in F)
    k = 1
    while True:
        k += 1
        if len(F) < 2:
            break
        # size-k square at (i,j) <=> size-(k-1) squares at (i,j),(i+1,j),(i,j+1),(i+1,j+1) all free
        G = []
        app = G.append
        for i in range(len(F) - 1):
            z = F[i] & F[i + 1]
            app(z & (z >> 1))
        F = G
        c = sum(popcount(x) for x in F)
        if c == 0:
            break
        total += c
    print(total)


main()
