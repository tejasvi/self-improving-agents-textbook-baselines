import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = 101
    S2 = S * S
    SIZE = S * S2
    vals = list(map(int, data[1:1 + 6 * n]))
    deg = [0] * (n + 1)
    pairs = set()
    for a in range(3):
        p, q = [t for t in range(3) if t != a]
        A = [0] * SIZE  # cuboid whose max face on plane c covers cell (u,v)
        B = [0] * SIZE  # cuboid whose min face on plane c covers cell (u,v)
        for i in range(n):
            base = 6 * i
            lo = (vals[base + a], vals[base + p], vals[base + q])
            hi = (vals[base + 3 + a], vals[base + 3 + p], vals[base + 3 + q])
            cid = i + 1
            v1, v2 = lo[2], hi[2]
            w = v2 - v1
            row = [cid] * w
            ca = hi[0] * S2
            cb = lo[0] * S2
            for u in range(lo[1], hi[1]):
                o = u * S + v1
                A[ca + o: ca + o + w] = row
                B[cb + o: cb + o + w] = row
        for x, y in set(zip(A, B)):
            if x and y:
                if x < y:
                    pairs.add((x, y))
                else:
                    pairs.add((y, x))
    for x, y in pairs:
        deg[x] += 1
        deg[y] += 1
    sys.stdout.write("\n".join(str(deg[i]) for i in range(1, n + 1)) + "\n")


main()
