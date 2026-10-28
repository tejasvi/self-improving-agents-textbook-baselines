import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    out = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(m):
        a = int(data[idx]); b = int(data[idx + 1]); c = int(data[idx + 2])
        idx += 3
        out[a].append((b, c))

    # weighted union-find with parity: par[v] ^ value(v) = value(root)
    parent = list(range(n + 1))
    rel = [0] * (n + 1)  # parity from v to parent

    def find(v):
        # returns (root, parity of v relative to root), with path compression
        path = []
        while parent[v] != v:
            path.append(v)
            v = parent[v]
        root = v
        # compress: process from closest-to-root to farthest
        acc = 0
        for u in reversed(path):
            acc ^= rel[u]
            rel[u] = acc
            parent[u] = root
        return root

    def parity(v):
        find(v)
        return rel[v] if parent[v] != v else 0

    for a in range(1, n + 1):
        lst = out[a]
        if len(lst) < 2:
            continue
        b0, c0 = lst[0]
        for bj, cj in lst[1:]:
            need = c0 ^ cj  # h_b0 ^ h_bj = need
            r1 = find(b0)
            p1 = rel[b0] if parent[b0] != b0 else 0
            r2 = find(bj)
            p2 = rel[bj] if parent[bj] != bj else 0
            if r1 == r2:
                if (p1 ^ p2) != need:
                    print(-1)
                    return
            else:
                # attach r2 under r1 with parity so that p1 ^ rel ^ p2 = need
                parent[r2] = r1
                rel[r2] = p1 ^ p2 ^ need

    h = [0] * (n + 1)
    for v in range(1, n + 1):
        h[v] = parity(v)  # root value 0 (roots have rel 0)

    res = ['0'] * n
    for a in range(1, n + 1):
        if out[a]:
            b0, c0 = out[a][0]
            res[a - 1] = str(c0 ^ h[b0] ^ h[a])
    print(''.join(res))


main()
