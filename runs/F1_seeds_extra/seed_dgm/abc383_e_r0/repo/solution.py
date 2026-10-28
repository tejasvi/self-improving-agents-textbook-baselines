import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); m = int(data[idx + 1]); k = int(data[idx + 2])
    idx += 3
    edges = []
    for _ in range(m):
        u = int(data[idx]); v = int(data[idx + 1]); w = int(data[idx + 2])
        idx += 3
        edges.append((w, u, v))
    A = data[idx:idx + k]; idx += k
    B = data[idx:idx + k]; idx += k

    cA = [0] * (n + 1)
    cB = [0] * (n + 1)
    for x in A:
        cA[int(x)] += 1
    for x in B:
        cB[int(x)] += 1

    parent = list(range(n + 1))

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    edges.sort()
    S = 0  # sum over components of min(a, b)
    prev = 0
    ans = 0
    i = 0
    while i < m:
        w = edges[i][0]
        # pairs with f >= w contribute (w - prev) each
        ans += (w - prev) * (k - S)
        prev = w
        while i < m and edges[i][0] == w:
            _, u, v = edges[i]
            i += 1
            ru = find(u); rv = find(v)
            if ru == rv:
                continue
            a1, b1 = cA[ru], cB[ru]
            a2, b2 = cA[rv], cB[rv]
            S -= min(a1, b1) + min(a2, b2)
            parent[rv] = ru
            cA[ru] = a1 + a2
            cB[ru] = b1 + b2
            S += min(cA[ru], cB[ru])
    print(ans)


main()
