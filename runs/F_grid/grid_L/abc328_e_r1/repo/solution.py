import sys


def main():
    data = sys.stdin.read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    edges = []
    idx = 3
    for _ in range(m):
        u = int(data[idx]) - 1
        v = int(data[idx + 1]) - 1
        w = int(data[idx + 2])
        idx += 3
        edges.append((u, v, w))

    best = [None]

    # comp[i] = component label of vertex i; relabel on merge
    def rec(i, comp, count, total):
        # count = number of tree edges chosen so far
        if count == n - 1:
            val = total % k
            if best[0] is None or val < best[0]:
                best[0] = val
            return
        if m - i < (n - 1) - count:
            return
        u, v, w = edges[i]
        cu, cv = comp[u], comp[v]
        if cu != cv:
            new = [cu if c == cv else c for c in comp]
            rec(i + 1, new, count + 1, total + w)
        rec(i + 1, comp, count, total)

    rec(0, list(range(n)), 0, 0)
    print(best[0])


main()
