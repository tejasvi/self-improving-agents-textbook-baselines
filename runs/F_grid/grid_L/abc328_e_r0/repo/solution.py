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
    need = n - 1

    # comp[x] = component label of vertex x
    def dfs(i, comp, cnt, total):
        if cnt == need:
            val = total % k
            if best[0] is None or val < best[0]:
                best[0] = val
            return
        if m - i < need - cnt:
            return
        u, v, w = edges[i]
        cu, cv = comp[u], comp[v]
        if cu != cv:
            # include edge i: merge cv into cu
            newcomp = tuple(cu if c == cv else c for c in comp)
            dfs(i + 1, newcomp, cnt + 1, total + w)
        # exclude edge i
        dfs(i + 1, comp, cnt, total)

    dfs(0, tuple(range(n)), 0, 0)
    print(best[0])


main()
