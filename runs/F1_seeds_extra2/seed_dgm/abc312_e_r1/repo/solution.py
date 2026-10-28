import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cubs = []
    idx = 1
    for _ in range(n):
        vals = list(map(int, data[idx:idx + 6]))
        idx += 6
        lo = (vals[0], vals[1], vals[2])
        hi = (vals[3], vals[4], vals[5])
        cubs.append((lo, hi))

    pairs = set()
    S = 101
    for a in range(3):
        b, c = [t for t in range(3) if t != a]
        # plus[plane] : grid over (b,c) of cuboid id whose max face is at plane
        # minus[plane]: grid over (b,c) of cuboid id whose min face is at plane
        plus = {}
        minus = {}
        for k, (lo, hi) in enumerate(cubs):
            wb = hi[b] - lo[b]
            wc = hi[c] - lo[c]
            for store, plane in ((plus, hi[a]), (minus, lo[a])):
                g = store.get(plane)
                if g is None:
                    g = [[-1] * S for _ in range(S)]
                    store[plane] = g
                for u in range(lo[b], hi[b]):
                    g[u][lo[c]:hi[c]] = [k] * wc
        for plane, pg in plus.items():
            mg = minus.get(plane)
            if mg is None:
                continue
            for pr, mr in zip(pg, mg):
                for p, m in zip(pr, mr):
                    if p >= 0 and m >= 0:
                        pairs.add((p, m) if p < m else (m, p))

    deg = [0] * n
    for p, m in pairs:
        deg[p] += 1
        deg[m] += 1
    sys.stdout.write("\n".join(map(str, deg)) + "\n")


main()
