import sys
from array import array


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cubes = []
    vals = list(map(int, data[1:1 + 6 * n]))
    for i in range(n):
        b = 6 * i
        lo = (vals[b], vals[b + 1], vals[b + 2])
        hi = (vals[b + 3], vals[b + 4], vals[b + 5])
        cubes.append((lo, hi))

    # H[(a,c)]: grid of cuboids whose max face on axis a is at c
    # L[(a,c)]: grid of cuboids whose min face on axis a is at c
    # grid cell index p*100+q over the two other axes (u,v)
    H = {}
    L = {}
    SZ = 100 * 100

    def fill(store, key, lo, hi, a, idx):
        g = store.get(key)
        if g is None:
            g = array('i', [0]) * SZ
            store[key] = g
        u, v = [x for x in range(3) if x != a]
        w = hi[v] - lo[v]
        seg = array('i', [idx]) * w
        for p in range(lo[u], hi[u]):
            base = p * 100
            g[base + lo[v]: base + hi[v]] = seg

    for idx in range(1, n + 1):
        lo, hi = cubes[idx - 1]
        for a in range(3):
            fill(H, (a, hi[a]), lo, hi, a, idx)
            fill(L, (a, lo[a]), lo, hi, a, idx)

    nb = [set() for _ in range(n + 1)]
    for idx in range(1, n + 1):
        lo, hi = cubes[idx - 1]
        s = nb[idx]
        for a in range(3):
            u, v = [x for x in range(3) if x != a]
            w0, w1 = lo[v], hi[v]
            # faces at hi[a]: matched by cuboids with lo[a] == hi[a]
            g = L.get((a, hi[a]))
            if g is not None:
                for p in range(lo[u], hi[u]):
                    base = p * 100
                    s.update(g[base + w0: base + w1])
            # faces at lo[a]: matched by cuboids with hi[a] == lo[a]
            g = H.get((a, lo[a]))
            if g is not None:
                for p in range(lo[u], hi[u]):
                    base = p * 100
                    s.update(g[base + w0: base + w1])
        s.discard(0)
        s.discard(idx)

    out = [str(len(nb[i])) for i in range(1, n + 1)]
    sys.stdout.write("\n".join(out) + "\n")


main()
